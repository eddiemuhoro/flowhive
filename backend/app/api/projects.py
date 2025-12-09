from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.workspace import WorkspaceMember
from app.models.project import Project, TaskList
from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectDetailResponse,
    TaskListCreate,
    TaskListUpdate,
    TaskListResponse
)
from app.utils.auth import get_current_active_user

router = APIRouter()


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new project"""
    # Check if user is workspace member
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == project_data.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    project = Project(**project_data.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)

    return project


@router.get("/workspace/{workspace_id}", response_model=List[ProjectResponse])
async def get_workspace_projects(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all projects in a workspace"""
    # Check if user is workspace member
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    projects = db.query(Project).filter(Project.workspace_id == workspace_id).all()
    return projects


@router.get("/{project_id}", response_model=ProjectDetailResponse)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific project with task lists"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # Check if user is workspace member
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == project.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    # Format task lists with tasks including assignee names
    from app.models.task import Task
    formatted_task_lists = []
    for task_list in project.task_lists:
        tasks_with_names = []
        for task in task_list.tasks:
            task_dict = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "task_list_id": task.task_list_id,
                "parent_task_id": task.parent_task_id,
                "creator_id": task.creator_id,
                "assignee_id": task.assignee_id,
                "status": task.status,
                "priority": task.priority,
                "due_date": task.due_date,
                "start_date": task.start_date,
                "completed_at": task.completed_at,
                "position": task.position,
                "estimated_hours": task.estimated_hours,
                "actual_hours": task.actual_hours,
                "created_at": task.created_at,
                "updated_at": task.updated_at,
                "assignee_name": None,
                "creator_name": None
            }

            # Get assignee name
            if task.assignee_id:
                assignee = db.query(User).filter(User.id == task.assignee_id).first()
                if assignee:
                    task_dict["assignee_name"] = assignee.full_name or assignee.username

            # Get creator name
            creator = db.query(User).filter(User.id == task.creator_id).first()
            if creator:
                task_dict["creator_name"] = creator.full_name or creator.username

            tasks_with_names.append(task_dict)

        formatted_task_lists.append({
            "id": task_list.id,
            "name": task_list.name,
            "description": task_list.description,
            "project_id": task_list.project_id,
            "position": task_list.position,
            "created_at": task_list.created_at,
            "updated_at": task_list.updated_at,
            "tasks": tasks_with_names
        })

    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "workspace_id": project.workspace_id,
        "color": project.color,
        "icon": project.icon,
        "created_at": project.created_at,
        "updated_at": project.updated_at,
        "task_lists": formatted_task_lists
    }

@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # Check if user is workspace member
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == project.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    update_data = project_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # Check if user is workspace member
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == project.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    db.delete(project)
    db.commit()
    return None


# Task List endpoints
@router.post("/task-lists", response_model=TaskListResponse, status_code=status.HTTP_201_CREATED)
async def create_task_list(
    task_list_data: TaskListCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new task list"""
    project = db.query(Project).filter(Project.id == task_list_data.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # Check if user is workspace member
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == project.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    task_list = TaskList(**task_list_data.model_dump())
    db.add(task_list)
    db.commit()
    db.refresh(task_list)

    return task_list


@router.patch("/task-lists/{task_list_id}", response_model=TaskListResponse)
async def update_task_list(
    task_list_id: int,
    task_list_data: TaskListUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a task list"""
    task_list = db.query(TaskList).filter(TaskList.id == task_list_id).first()
    if not task_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task list not found"
        )

    update_data = task_list_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task_list, field, value)

    db.commit()
    db.refresh(task_list)
    return task_list


@router.delete("/task-lists/{task_list_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_list(
    task_list_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a task list"""
    task_list = db.query(TaskList).filter(TaskList.id == task_list_id).first()
    if not task_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task list not found"
        )

    db.delete(task_list)
    db.commit()
    return None
