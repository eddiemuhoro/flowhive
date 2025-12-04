from typing import List
import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.comment import Attachment
from app.schemas.comment import AttachmentResponse
from app.utils.auth import get_current_active_user
from app.config import settings
import aiofiles

router = APIRouter()


ALLOWED_EXTENSIONS = {
    "image/jpeg", "image/png", "image/gif", "image/webp",
    "application/pdf", "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "text/plain", "text/csv"
}


@router.post("/", response_model=AttachmentResponse, status_code=status.HTTP_201_CREATED)
async def upload_attachment(
    task_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Upload a file attachment to a task"""
    # Validate file size
    file_content = await file.read()
    file_size = len(file_content)

    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE} bytes"
        )

    # Validate file type
    if file.content_type not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file.content_type} not allowed"
        )

    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

    # Save file
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(file_content)

    # Create attachment record
    attachment = Attachment(
        filename=unique_filename,
        original_filename=file.filename,
        file_path=file_path,
        file_size=file_size,
        mime_type=file.content_type,
        task_id=task_id,
        uploaded_by=current_user.id
    )

    db.add(attachment)
    db.commit()
    db.refresh(attachment)

    # Add uploader info to response
    response = AttachmentResponse.model_validate(attachment)
    response.uploader_name = current_user.full_name or current_user.username

    return response


@router.get("/task/{task_id}", response_model=List[AttachmentResponse])
async def get_task_attachments(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all attachments for a task"""
    attachments = db.query(Attachment).filter(Attachment.task_id == task_id).all()

    # Add uploader info to each attachment
    response_attachments = []
    for attachment in attachments:
        attachment_response = AttachmentResponse.model_validate(attachment)
        if attachment.uploader:
            attachment_response.uploader_name = attachment.uploader.full_name or attachment.uploader.username
        response_attachments.append(attachment_response)

    return response_attachments


@router.delete("/{attachment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attachment(
    attachment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete an attachment"""
    attachment = db.query(Attachment).filter(Attachment.id == attachment_id).first()
    if not attachment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attachment not found"
        )

    if attachment.uploaded_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only delete your own attachments"
        )

    # Delete file from filesystem
    if os.path.exists(attachment.file_path):
        os.remove(attachment.file_path)

    db.delete(attachment)
    db.commit()
    return None
