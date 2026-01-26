from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app.models.user import User
from app.models.task import Task, TaskStatus
from app.models.comment import ActivityLog
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskDetailResponse
from app.utils.auth import get_current_active_user
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

    tasks = query.offset(skip).limit(limit).all()
    return tasks


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

    db.delete(task)
    db.commit()

    # Log activity
    log_activity(db, task.id, current_user.id, "deleted", {
        "title": task.title
    })
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
