from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from app.utils.auth import get_current_active_user

router = APIRouter()


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new comment"""
    comment = Comment(
        content=comment_data.content,
        task_id=comment_data.task_id,
        user_id=current_user.id,
        parent_comment_id=comment_data.parent_comment_id
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    # Add user info to response
    response = CommentResponse.model_validate(comment)
    response.user_name = current_user.full_name or current_user.username
    response.user_avatar = current_user.avatar_url

    return response


@router.get("/task/{task_id}", response_model=List[CommentResponse])
async def get_task_comments(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all comments for a task"""
    comments = db.query(Comment).filter(Comment.task_id == task_id).order_by(Comment.created_at).all()

    # Add user info to each comment
    response_comments = []
    for comment in comments:
        comment_response = CommentResponse.model_validate(comment)
        if comment.user:
            comment_response.user_name = comment.user.full_name or comment.user.username
            comment_response.user_avatar = comment.user.avatar_url
        response_comments.append(comment_response)

    return response_comments


@router.patch("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a comment"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only edit your own comments"
        )

    comment.content = comment_data.content
    db.commit()
    db.refresh(comment)

    response = CommentResponse.model_validate(comment)
    response.user_name = current_user.full_name or current_user.username
    response.user_avatar = current_user.avatar_url

    return response


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a comment"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only delete your own comments"
        )

    db.delete(comment)
    db.commit()
    return None
