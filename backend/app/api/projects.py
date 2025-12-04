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

    return project


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
