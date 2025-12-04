from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    task_id: int
    parent_comment_id: Optional[int] = None


class CommentUpdate(BaseModel):
    content: str


class CommentResponse(CommentBase):
    id: int
    task_id: int
    user_id: int
    parent_comment_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    user_name: Optional[str] = None
    user_avatar: Optional[str] = None

    class Config:
        from_attributes = True


class AttachmentResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_path: str
    file_size: int
    mime_type: str
    task_id: int
    uploaded_by: int
    uploader_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ActivityLogResponse(BaseModel):
    id: int
    task_id: int
    user_id: int
    user_name: Optional[str] = None
    action: str
    details: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
