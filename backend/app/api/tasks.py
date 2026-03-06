from typing import Dict, List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
import httpx
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app.models.user import User
from app.models.task import Task, TaskStatus
from app.models.comment import ActivityLog
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskDetailResponse
from app.utils.auth import get_current_active_user
from app.config import Settings
import json

router = APIRouter()


def log_activity(db: Session, task_id: int, user_id: int, action: str, details: dict = None):
    """Helper to log task activity"""
    activity = ActivityLog(
        task_id=task_id,
        user_id=user_id,
        action=action,
        details=json.dumps(details) if details else None
    )
    db.add(activity)


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new task"""
    task = Task(
        **task_data.model_dump(),
        creator_id=current_user.id,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    # Log activity
    log_activity(db, task.id, current_user.id, "created", {
        "title": task.title,
        "status": task.status.value
    })
    db.commit()

    return task

@router.get("/github-repos", response_model=List[Dict])
async def get_github_repos(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get list of GitHub repositories accessible to the user
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{Settings().GITHUB_API_URL}/user/repos?per_page=100&sort=updated",
                headers={"Authorization": f"Bearer {Settings().GITHUB_API_TOKEN}"}
            )
            response.raise_for_status()
            repos = response.json()
            return [
                {
                    "name": repo["name"],
                    "full_name": repo["full_name"],
                    "owner": repo["owner"]["login"],
                    "description": repo.get("description", ""),
                    "private": repo["private"],
                    "url": repo["html_url"]
                }
                for repo in repos
            ]
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to fetch repos from GitHub: {str(e)}"
        )


@router.get("/github-commits", response_model=List[Dict])
async def get_github_commits(
    repo_owner: str = Query(..., description="Repository owner"),
    repo_name: str = Query(..., description="Repository name"),
    since: Optional[str] = Query(None, description="Only commits after this date (ISO 8601)"),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get recent commits from GitHub for the specified repository
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            url = f"{Settings().GITHUB_API_URL}/{repo_owner}/{repo_name}/commits?author={current_user.username}&per_page=100"
            if since:
                url += f"&since={since}"

            response = await client.get(
                url,
                headers={"Authorization": f"Bearer {Settings().GITHUB_API_TOKEN}"}
            )
            response.raise_for_status()
            commits = response.json()
            return [
                    {
                        "sha": commit["sha"],
                        "message": commit["commit"]["message"],
                        "url": commit["html_url"],
                        "date": commit["commit"]["author"]["date"],
                        "author": commit["commit"]["author"]["name"]
                    }
                    for commit in commits
            ]
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to fetch commits from GitHub: {str(e)}"
        )


@router.post("/create-tasks-from-github", response_model=List[TaskResponse])
async def create_tasks_from_github_commits(
    project_id: int = Query(..., description="Project ID to create tasks in"),
    repo_owner: str = Query(..., description="Repository owner"),
    repo_name: str = Query(..., description="Repository name"),
    commit_shas: Optional[List[str]] = Query(None, description="Specific commit SHAs to import"),
    since: Optional[str] = Query(None, description="Only commits after this date (ISO 8601)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Fetch recent GitHub commits and create tasks from them.
    Use this at the end of the day to automatically log your work as tasks.
    Can either import specific commits by SHA or all commits since a date.
    """
    # Verify project exists and user has access
    from app.models.project import Project
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    try:
        # Fetch commits from GitHub
        async with httpx.AsyncClient(timeout=30.0) as client:
            url = f"{Settings().GITHUB_API_URL}/{repo_owner}/{repo_name}/commits?author={current_user.username}&per_page=100"
            if since:
                url += f"&since={since}"

            response = await client.get(
                url,
                headers={"Authorization": f"Bearer {Settings().GITHUB_API_TOKEN}"}
            )
            response.raise_for_status()
            commits = response.json()

        # Filter commits by SHA if specific commits were requested
        if commit_shas:
            commits = [c for c in commits if c["sha"] in commit_shas]

        # Create tasks from commits
        created_tasks = []
        for commit in commits:
            commit_message = commit["commit"]["message"]
            commit_sha = commit["sha"][:7]  # Short SHA
            commit_url = commit["html_url"]
            commit_date = commit["commit"]["author"]["date"]

            # Parse commit date and calculate start date (2 days before commit)
            commit_datetime = datetime.fromisoformat(commit_date.replace('Z', '+00:00'))
            start_datetime = commit_datetime - timedelta(days=2)

            # Create description with commit details
            description = f"{commit_message}\n\nCommit: {commit_sha}\nURL: {commit_url}\nDate: {commit_date}"

            # Create task
            task = Task(
                title=commit_message.split('\n')[0][:255],  # First line as title, limit to 255 chars
                description=description,
                project_id=project_id,
                creator_id=current_user.id,
                status=TaskStatus.COMPLETED,  # Mark as completed since work is done
                completed_at=commit_datetime,
                due_date=commit_datetime,  # Due date is the commit date
                start_date=start_datetime  # Start date is 2 days before commit
            )

            db.add(task)
            db.flush()  # Get the task ID

            # Log activity
            log_activity(db, task.id, current_user.id, "created_from_github", {
                "title": task.title,
                "commit_sha": commit_sha,
                "commit_url": commit_url
            })

            created_tasks.append(task)

        db.commit()

        # Refresh and prepare response
        response_tasks = []
        for task in created_tasks:
            db.refresh(task)
            task_response = TaskResponse.model_validate(task)
            if task.creator:
                task_response.creator_name = task.creator.full_name or task.creator.username
            response_tasks.append(task_response)

        return response_tasks

    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to fetch commits from GitHub: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create tasks: {str(e)}"
        )


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    project_id: Optional[int] = None,
    assignee_id: Optional[int] = None,
    status: Optional[TaskStatus] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get tasks with optional filters"""
    query = db.query(Task)

    if project_id:
        query = query.filter(Task.project_id == project_id)

    if assignee_id:
        query = query.filter(Task.assignee_id == assignee_id)

    if status:
        query = query.filter(Task.status == status)

    tasks = query.order_by(Task.updated_at.desc()).offset(skip).limit(limit).all()

    response_tasks = []
    for task in tasks:
        task_response = TaskResponse.model_validate(task)
        if task.assignee:
            task_response.assignee_name = task.assignee.full_name or task.assignee.username
        if task.creator:
            task_response.creator_name = task.creator.full_name or task.creator.username

        response_tasks.append(task_response)

    return response_tasks


@router.get("/my-tasks", response_model=List[TaskResponse])
async def get_my_tasks(
    status: Optional[TaskStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get tasks assigned to current user"""
    query = db.query(Task).filter(Task.assignee_id == current_user.id)

    if status:
        query = query.filter(Task.status == status)

    tasks = query.all()

    # Enrich tasks with names
    response_tasks = []
    for task in tasks:
        task_response = TaskResponse.model_validate(task)
        if task.assignee:
            task_response.assignee_name = task.assignee.full_name or task.assignee.username
        if task.creator:
            task_response.creator_name = task.creator.full_name or task.creator.username
        response_tasks.append(task_response)

    return response_tasks


@router.get("/{task_id}", response_model=TaskDetailResponse)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific task with details"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Get workspace_id through project -> workspace
    from app.models.project import Project
    workspace_id = None
    project = db.query(Project).filter(Project.id == task.project_id).first()
    if project:
        workspace_id = project.workspace_id

    # Add names for response
    response_data = TaskDetailResponse.model_validate(task)
    response_data.workspace_id = workspace_id
    if task.assignee:
        response_data.assignee_name = task.assignee.full_name or task.assignee.username
    if task.creator:
        response_data.creator_name = task.creator.full_name or task.creator.username

    return response_data


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a task"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Track changes for activity log
    changes = {}
    update_data = task_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        old_value = getattr(task, field)
        if old_value != value:
            changes[field] = {"old": str(old_value), "new": str(value)}
            setattr(task, field, value)

    # Mark as completed if status changed to completed
    if task_data.status == TaskStatus.COMPLETED and task.status != TaskStatus.COMPLETED:
        task.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(task)

    # Log activity
    if changes:
        log_activity(db, task.id, current_user.id, "updated", changes)
        db.commit()

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a task"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Log activity
    # log_activity(db, task.id, current_user.id, "deleted", {
    #     "title": task.title
    # })
    # db.commit()
    db.delete(task)
    db.commit()

    return None


@router.get("/{task_id}/subtasks", response_model=List[TaskResponse])
async def get_subtasks(
    task_id: int,
    db: Session = Depends(get_db),
):
    """Get all subtasks of a task"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    subtasks = db.query(Task).filter(Task.parent_task_id == task_id).all()
    return subtasks
