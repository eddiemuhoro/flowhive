from typing import List
import logging
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
from app.api.websocket import notify_workspace
from app.services.push_notification_service import PushNotificationService

router = APIRouter()
logger = logging.getLogger(__name__)


def format_comment_title(content: str, max_len: int = 80) -> str:
    cleaned = " ".join((content or "").split())
    if len(cleaned) <= max_len:
        return cleaned
    return f"{cleaned[:max_len - 1].rstrip()}…"


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

    await notify_workspace(activity.workspace_id, "field_activity_comment_added", {
        "activity_id": activity.id,
        "comment_id": comment.id,
        "user_id": current_user.id,
        "user_name": response.user_name,
        "target_user_ids": [activity.created_by, activity.support_staff_id],
    })

    push_targets = {
        activity.support_staff_id,
        activity.created_by,
    }

    for user_id in push_targets:
        try:
            sent = PushNotificationService.send_notification(
                db=db,
                user_id=user_id,
                title=format_comment_title(response.content) or "New Activity Comment",
                message=f"{response.user_name} commented on {activity.title}",
                data={
                    "tag": f"field-activity-comment-{activity.id}",
                    "url": f"/field/activities/{activity.id}",
                },
            )
            logger.info(
                "Push notification for field activity comment sent=%s user_id=%s activity_id=%s comment_id=%s",
                sent,
                user_id,
                activity.id,
                comment.id,
            )
        except Exception:
            logger.exception(
                "Failed to send push notification user_id=%s activity_id=%s comment_id=%s",
                user_id,
                activity.id,
                comment.id,
            )

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
