"""
Meeting Minutes Schemas
Pydantic schemas for meeting minutes API
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, time, datetime


# Attendee schemas
class Attendee(BaseModel):
    """Schema for meeting attendee"""
    id: Optional[int] = None
    name: str


# Action Item schemas
class ActionItemBase(BaseModel):
    """Base schema for action items"""
    description: str
    assigned_to: Optional[int] = None
    due_date: Optional[date] = None
    status: str = "pending"


class ActionItemCreate(ActionItemBase):
    """Schema for creating action items"""
    pass


class ActionItemUpdate(BaseModel):
    """Schema for updating action items"""
    description: Optional[str] = None
    assigned_to: Optional[int] = None
    due_date: Optional[date] = None
    status: Optional[str] = None


class ActionItemResponse(ActionItemBase):
    """Schema for action item response"""
    id: int
    meeting_minute_id: int
    created_at: datetime
    completed_at: Optional[datetime] = None
    assigned_user_name: Optional[str] = None

    class Config:
        from_attributes = True


# Attachment schemas
class AttachmentResponse(BaseModel):
    """Schema for minute attachment response"""
    id: int
    meeting_minute_id: int
    cloudinary_public_id: str
    cloudinary_url: str
    resource_type: str
    file_name: str
    file_size: int
    mime_type: str
    uploaded_by: int
    uploaded_at: datetime
    uploader_name: Optional[str] = None

    class Config:
        from_attributes = True


# Meeting Minute schemas
class MeetingMinuteBase(BaseModel):
    """Base schema for meeting minutes"""
    title: str
    meeting_date: date
    meeting_time_start: Optional[time] = None
    meeting_time_end: Optional[time] = None
    location: Optional[str] = None
    attendees: Optional[List[Attendee]] = None
    agenda: Optional[str] = None
    discussions: Optional[str] = None
    decisions: Optional[str] = None


class MeetingMinuteCreate(MeetingMinuteBase):
    """Schema for creating meeting minutes"""
    workspace_id: int
    action_items: Optional[List[ActionItemCreate]] = None


class MeetingMinuteUpdate(BaseModel):
    """Schema for updating meeting minutes"""
    title: Optional[str] = None
    meeting_date: Optional[date] = None
    meeting_time_start: Optional[time] = None
    meeting_time_end: Optional[time] = None
    location: Optional[str] = None
    attendees: Optional[List[Attendee]] = None
    agenda: Optional[str] = None
    discussions: Optional[str] = None
    decisions: Optional[str] = None


class MeetingMinuteResponse(MeetingMinuteBase):
    """Schema for meeting minute response (list view)"""
    id: int
    workspace_id: int
    created_by: int
    created_at: datetime
    updated_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    created_by_name: Optional[str] = None
    updated_by_name: Optional[str] = None
    attachment_count: int = 0
    action_item_count: int = 0

    class Config:
        from_attributes = True


class MeetingMinuteDetailResponse(MeetingMinuteResponse):
    """Schema for detailed meeting minute response (includes attachments and action items)"""
    attachments: List[AttachmentResponse] = []
    action_items: List[ActionItemResponse] = []

    class Config:
        from_attributes = True
