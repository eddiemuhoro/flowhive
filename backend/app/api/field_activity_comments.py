from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.field_activity import FieldActivity, FieldActivityComment
from app.schemas.field_activity import (
    FieldActivityCommentCreate,
    FieldActivityCommentUpdate,
    FieldActivityCommentResponse,
)
from app.utils.auth import get_current_active_user
from app.utils.sanitizer import sanitize_html
from app.api.field_operations import check_workspace_access

router = APIRouter()


def get_activity_or_404(activity_id: int, db: Session) -> FieldActivity:
    activity = db.query(FieldActivity).filter(FieldActivity.id == activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Field activity not found",
        )
    return activity


def ensure_assigned_activity(activity: FieldActivity) -> None:
    if activity.created_by == activity.support_staff_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Comments are only available for assigned tasks",
        )


def ensure_participant(activity: FieldActivity, current_user: User) -> None:
    if current_user.id not in {activity.created_by, activity.support_staff_id}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the task creator or assignee can access comments",
        )


@router.get("/{activity_id}/comments", response_model=List[FieldActivityCommentResponse])
async def get_activity_comments(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    activity = get_activity_or_404(activity_id, db)
    check_workspace_access(activity.workspace_id, current_user, db)
    ensure_assigned_activity(activity)
    ensure_participant(activity, current_user)

    comments = (
        db.query(FieldActivityComment)
        .filter(FieldActivityComment.field_activity_id == activity_id)
        .order_by(FieldActivityComment.created_at)
        .all()
    )

    response_comments = []
    for comment in comments:
        comment_response = FieldActivityCommentResponse.model_validate(comment)
        if comment.user:
            comment_response.user_name = comment.user.full_name or comment.user.username
            comment_response.user_avatar = comment.user.avatar_url
        response_comments.append(comment_response)

    return response_comments


@router.post(
    "/{activity_id}/comments",
    response_model=FieldActivityCommentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_activity_comment(
    activity_id: int,
    comment_data: FieldActivityCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    activity = get_activity_or_404(activity_id, db)
    check_workspace_access(activity.workspace_id, current_user, db)
    ensure_assigned_activity(activity)
    ensure_participant(activity, current_user)

    parent_comment_id = comment_data.parent_comment_id
    if parent_comment_id:
        parent_comment = (
            db.query(FieldActivityComment)
            .filter(FieldActivityComment.id == parent_comment_id)
            .first()
        )
        if not parent_comment or parent_comment.field_activity_id != activity_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid parent comment",
            )

    content = sanitize_html(comment_data.content)
    comment = FieldActivityComment(
        field_activity_id=activity_id,
        user_id=current_user.id,
        parent_comment_id=parent_comment_id,
        content=content,
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    response = FieldActivityCommentResponse.model_validate(comment)
    response.user_name = current_user.full_name or current_user.username
    response.user_avatar = current_user.avatar_url

    return response


@router.patch("/comments/{comment_id}", response_model=FieldActivityCommentResponse)
async def update_activity_comment(
    comment_id: int,
    comment_data: FieldActivityCommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    comment = db.query(FieldActivityComment).filter(FieldActivityComment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    activity = get_activity_or_404(comment.field_activity_id, db)
    check_workspace_access(activity.workspace_id, current_user, db)
    ensure_assigned_activity(activity)
    ensure_participant(activity, current_user)

    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only edit your own comments",
        )

    comment.content = sanitize_html(comment_data.content)
    db.commit()
    db.refresh(comment)

    response = FieldActivityCommentResponse.model_validate(comment)
    response.user_name = current_user.full_name or current_user.username
    response.user_avatar = current_user.avatar_url

    return response


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_activity_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    comment = db.query(FieldActivityComment).filter(FieldActivityComment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    activity = get_activity_or_404(comment.field_activity_id, db)
    check_workspace_access(activity.workspace_id, current_user, db)
    ensure_assigned_activity(activity)
    ensure_participant(activity, current_user)

    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only delete your own comments",
        )

    db.delete(comment)
    db.commit()
    return None
