from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.workspace import WorkspaceMember
from app.models.field_activity import TaskCategory
from app.schemas.field_activity import (
    TaskCategoryCreate,
    TaskCategoryUpdate,
    TaskCategoryResponse
)
from app.utils.auth import get_current_active_user

router = APIRouter()


@router.post("/", response_model=TaskCategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_task_category(
    category_data: TaskCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new task category"""
    # Check if user is workspace member
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == category_data.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    # Create category with created_by automatically set
    category_dict = category_data.model_dump()
    category_dict['created_by'] = current_user.id
    category = TaskCategory(**category_dict)
    db.add(category)
    db.commit()
    db.refresh(category)

    return category


@router.get("/workspace/{workspace_id}", response_model=List[TaskCategoryResponse])
async def get_workspace_task_categories(
    workspace_id: int,
    include_inactive: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all task categories for a workspace"""
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

    query = db.query(TaskCategory).filter(TaskCategory.workspace_id == workspace_id)

    if not include_inactive:
        query = query.filter(TaskCategory.is_active == True)

    categories = query.order_by(TaskCategory.name).all()
    return categories


@router.get("/{category_id}", response_model=TaskCategoryResponse)
async def get_task_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific task category"""
    category = db.query(TaskCategory).filter(TaskCategory.id == category_id).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task category not found"
        )

    # Check if user is workspace member
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == category.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    return category


@router.put("/{category_id}", response_model=TaskCategoryResponse)
async def update_task_category(
    category_id: int,
    category_data: TaskCategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a task category"""
    category = db.query(TaskCategory).filter(TaskCategory.id == category_id).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task category not found"
        )

    # Check if user is workspace member
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == category.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    # Update category fields
    update_data = category_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)

    db.commit()
    db.refresh(category)

    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete (deactivate) a task category"""
    category = db.query(TaskCategory).filter(TaskCategory.id == category_id).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task category not found"
        )

    # Check if user is workspace member
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == category.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    # Soft delete - deactivate instead of removing
    category.is_active = False
    db.commit()

    return None
