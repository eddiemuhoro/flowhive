"""
Meeting Minutes API endpoints
Handles CRUD operations for meeting minutes with Cloudinary file uploads
"""
from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.database import get_db
from app.models.user import User, UserRole
from app.models.workspace import WorkspaceMember
from app.models.meeting_minute import MeetingMinute, MinuteAttachment, MinuteActionItem
from app.schemas.meeting_minute import (
    MeetingMinuteCreate,
    MeetingMinuteUpdate,
    MeetingMinuteResponse,
    MeetingMinuteDetailResponse,
    AttachmentResponse,
    ActionItemCreate,
    ActionItemUpdate,
    ActionItemResponse
)
from app.utils.auth import get_current_active_user, require_role
from app.utils.sanitizer import sanitize_html
from app.utils.cloudinary import upload_to_cloudinary, delete_from_cloudinary
from app.config import settings

router = APIRouter()

ALLOWED_FILE_TYPES = {
    "application/pdf",
    "image/jpeg", "image/png", "image/gif", "image/webp",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}


@router.post("/", response_model=MeetingMinuteDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_meeting_minute(
    minute_data: MeetingMinuteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new meeting minute"""
    # Check workspace membership
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == minute_data.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    # Sanitize HTML content
    minute_dict = minute_data.model_dump(exclude={"action_items"})
    if minute_dict.get("agenda"):
        minute_dict["agenda"] = sanitize_html(minute_dict["agenda"])
    if minute_dict.get("discussions"):
        minute_dict["discussions"] = sanitize_html(minute_dict["discussions"])
    if minute_dict.get("decisions"):
        minute_dict["decisions"] = sanitize_html(minute_dict["decisions"])

    # Create meeting minute
    meeting_minute = MeetingMinute(
        **minute_dict,
        created_by=current_user.id
    )
    db.add(meeting_minute)
    db.flush()  # Get the ID without committing

    # Create action items if provided
    if minute_data.action_items:
        for action_item_data in minute_data.action_items:
            action_item = MinuteActionItem(
                meeting_minute_id=meeting_minute.id,
                **action_item_data.model_dump()
            )
            db.add(action_item)

    db.commit()
    db.refresh(meeting_minute)

    # Populate computed fields
    meeting_minute.created_by_name = current_user.full_name or current_user.username
    meeting_minute.attachment_count = 0
    meeting_minute.action_item_count = len(minute_data.action_items) if minute_data.action_items else 0

    # Populate action items with assigned user names
    for action_item in meeting_minute.action_items:
        if action_item.assigned_to:
            action_item.assigned_user_name = action_item.assigned_user.full_name or action_item.assigned_user.username

    return meeting_minute


@router.get("/workspace/{workspace_id}", response_model=List[MeetingMinuteResponse])
async def get_workspace_meeting_minutes(
    workspace_id: int,
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all meeting minutes for a workspace with optional filters"""
    # Check workspace membership
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    # Build query
    query = db.query(MeetingMinute).filter(MeetingMinute.workspace_id == workspace_id)

    # Apply filters
    if date_from:
        query = query.filter(MeetingMinute.meeting_date >= date_from)
    if date_to:
        query = query.filter(MeetingMinute.meeting_date <= date_to)
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            func.lower(MeetingMinute.title).like(search_pattern.lower())
        )

    # Order by date descending
    minutes = query.order_by(MeetingMinute.meeting_date.desc()).all()

    # Populate computed fields
    for minute in minutes:
        minute.created_by_name = minute.created_by_user.full_name or minute.created_by_user.username
        if minute.updated_by:
            minute.updated_by_name = minute.updated_by_user.full_name or minute.updated_by_user.username
        minute.attachment_count = len(minute.attachments)
        minute.action_item_count = len(minute.action_items)

    return minutes


@router.get("/{minute_id}", response_model=MeetingMinuteDetailResponse)
async def get_meeting_minute(
    minute_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific meeting minute with full details"""
    minute = db.query(MeetingMinute).filter(MeetingMinute.id == minute_id).first()

    if not minute:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting minute not found"
        )

    # Check workspace membership
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == minute.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    # Populate computed fields
    minute.created_by_name = minute.created_by_user.full_name or minute.created_by_user.username
    if minute.updated_by:
        minute.updated_by_name = minute.updated_by_user.full_name or minute.updated_by_user.username
    minute.attachment_count = len(minute.attachments)
    minute.action_item_count = len(minute.action_items)

    # Populate action items
    for action_item in minute.action_items:
        if action_item.assigned_to:
            action_item.assigned_user_name = action_item.assigned_user.full_name or action_item.assigned_user.username

    # Populate attachments
    for attachment in minute.attachments:
        attachment.uploader_name = attachment.uploaded_by_user.full_name or attachment.uploaded_by_user.username

    return minute


@router.put("/{minute_id}", response_model=MeetingMinuteResponse)
async def update_meeting_minute(
    minute_id: int,
    minute_data: MeetingMinuteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a meeting minute"""
    minute = db.query(MeetingMinute).filter(MeetingMinute.id == minute_id).first()

    if not minute:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting minute not found"
        )

    # Check workspace membership
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == minute.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    # Update fields
    update_dict = minute_data.model_dump(exclude_unset=True)
    
    # Sanitize HTML content
    if "agenda" in update_dict and update_dict["agenda"]:
        update_dict["agenda"] = sanitize_html(update_dict["agenda"])
    if "discussions" in update_dict and update_dict["discussions"]:
        update_dict["discussions"] = sanitize_html(update_dict["discussions"])
    if "decisions" in update_dict and update_dict["decisions"]:
        update_dict["decisions"] = sanitize_html(update_dict["decisions"])

    for key, value in update_dict.items():
        setattr(minute, key, value)

    minute.updated_by = current_user.id

    db.commit()
    db.refresh(minute)

    # Populate computed fields
    minute.created_by_name = minute.created_by_user.full_name or minute.created_by_user.username
    minute.updated_by_name = current_user.full_name or current_user.username
    minute.attachment_count = len(minute.attachments)
    minute.action_item_count = len(minute.action_items)

    return minute


@router.delete("/{minute_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_meeting_minute(
    minute_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a meeting minute"""
    minute = db.query(MeetingMinute).filter(MeetingMinute.id == minute_id).first()

    if not minute:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting minute not found"
        )

    # Check workspace membership
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == minute.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    # Only allow deletion by creator or managers/executives
    if minute.created_by != current_user.id and current_user.role == UserRole.TEAM_MEMBER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the creator or managers can delete meeting minutes"
        )

    # Delete attachments from Cloudinary
    for attachment in minute.attachments:
        try:
            await delete_from_cloudinary(
                attachment.cloudinary_public_id,
                attachment.resource_type
            )
        except Exception as e:
            print(f"Failed to delete Cloudinary file: {e}")

    db.delete(minute)
    db.commit()


@router.post("/{minute_id}/attachments", response_model=AttachmentResponse, status_code=status.HTTP_201_CREATED)
async def upload_attachment(
    minute_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Upload an attachment (PDF, image, doc) to Cloudinary"""
    minute = db.query(MeetingMinute).filter(MeetingMinute.id == minute_id).first()

    if not minute:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting minute not found"
        )

    # Check workspace membership
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == minute.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    # Validate file
    file_content = await file.read()
    file_size = len(file_content)

    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum of {settings.MAX_UPLOAD_SIZE} bytes"
        )

    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file.content_type} not allowed"
        )

    # Determine resource type
    resource_type = "image" if file.content_type.startswith("image/") else "raw"

    # Upload to Cloudinary
    try:
        result = await upload_to_cloudinary(
            file_content,
            file.filename,
            folder="flowhive/minutes",
            resource_type=resource_type
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}"
        )

    # Create attachment record
    attachment = MinuteAttachment(
        meeting_minute_id=minute_id,
        cloudinary_public_id=result["public_id"],
        cloudinary_url=result["secure_url"],
        resource_type=resource_type,
        file_name=file.filename,
        file_size=file_size,
        mime_type=file.content_type,
        uploaded_by=current_user.id
    )

    db.add(attachment)
    db.commit()
    db.refresh(attachment)

    attachment.uploader_name = current_user.full_name or current_user.username

    return attachment


@router.delete("/{minute_id}/attachments/{attachment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attachment(
    minute_id: int,
    attachment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete an attachment from meeting minute and Cloudinary"""
    attachment = db.query(MinuteAttachment).filter(
        MinuteAttachment.id == attachment_id,
        MinuteAttachment.meeting_minute_id == minute_id
    ).first()

    if not attachment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attachment not found"
        )

    minute = attachment.meeting_minute

    # Check workspace membership
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == minute.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    # Delete from Cloudinary
    try:
        await delete_from_cloudinary(
            attachment.cloudinary_public_id,
            attachment.resource_type
        )
    except Exception as e:
        print(f"Failed to delete from Cloudinary: {e}")

    db.delete(attachment)
    db.commit()


@router.post("/{minute_id}/action-items", response_model=ActionItemResponse, status_code=status.HTTP_201_CREATED)
async def create_action_item(
    minute_id: int,
    action_item_data: ActionItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create an action item for a meeting minute"""
    minute = db.query(MeetingMinute).filter(MeetingMinute.id == minute_id).first()

    if not minute:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting minute not found"
        )

    # Check workspace membership
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == minute.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    action_item = MinuteActionItem(
        meeting_minute_id=minute_id,
        **action_item_data.model_dump()
    )

    db.add(action_item)
    db.commit()
    db.refresh(action_item)

    if action_item.assigned_to:
        action_item.assigned_user_name = action_item.assigned_user.full_name or action_item.assigned_user.username

    return action_item


@router.put("/{minute_id}/action-items/{action_item_id}", response_model=ActionItemResponse)
async def update_action_item(
    minute_id: int,
    action_item_id: int,
    action_item_data: ActionItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update an action item"""
    action_item = db.query(MinuteActionItem).filter(
        MinuteActionItem.id == action_item_id,
        MinuteActionItem.meeting_minute_id == minute_id
    ).first()

    if not action_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Action item not found"
        )

    minute = action_item.meeting_minute

    # Check workspace membership
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == minute.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    # Update fields
    update_dict = action_item_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(action_item, key, value)

    # Set completed_at if status changed to completed
    if "status" in update_dict and update_dict["status"] == "completed" and not action_item.completed_at:
        from datetime import datetime
        action_item.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(action_item)

    if action_item.assigned_to:
        action_item.assigned_user_name = action_item.assigned_user.full_name or action_item.assigned_user.username

    return action_item


@router.delete("/{minute_id}/action-items/{action_item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_action_item(
    minute_id: int,
    action_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete an action item"""
    action_item = db.query(MinuteActionItem).filter(
        MinuteActionItem.id == action_item_id,
        MinuteActionItem.meeting_minute_id == minute_id
    ).first()

    if not action_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Action item not found"
        )

    minute = action_item.meeting_minute

    # Check workspace membership
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == minute.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    db.delete(action_item)
    db.commit()
