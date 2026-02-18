from pydantic import BaseModel, field_validator, model_validator
from typing import Optional, List
from datetime import datetime, date, time
from app.schemas.user import UserResponse
from app.models.field_activity import ActivityStatus, LocationType


# Minimal user info for creator/updater fields
class UserBasicInfo(BaseModel):
    id: int
    username: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True


# TaskCategory Schemas
class TaskCategoryBase(BaseModel):
    name: str
    title: str
    description: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    required_role: str = "team_member"  # team_member, manager, or executive


class TaskCategoryCreate(TaskCategoryBase):
    workspace_id: int


class TaskCategoryUpdate(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    required_role: Optional[str] = None
    is_active: Optional[bool] = None


class TaskCategoryResponse(TaskCategoryBase):
    id: int
    workspace_id: int
    is_active: bool
    created_by: Optional[int] = None
    created_by_user: Optional[UserBasicInfo] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# FieldActivityPhoto Schemas
class FieldActivityPhotoBase(BaseModel):
    file_name: str
    file_path: str
    file_size: int
    mime_type: str


class FieldActivityPhotoCreate(BaseModel):
    # File upload handled separately, this is for metadata
    pass


class FieldActivityPhotoResponse(FieldActivityPhotoBase):
    id: int
    field_activity_id: int
    uploaded_by: int
    uploaded_at: datetime

    class Config:
        from_attributes = True


# FieldActivity Schemas
class FieldActivityBase(BaseModel):
    activity_date: date
    start_time: Optional[time] = None  # Required only for COMPLETED status
    end_time: Optional[time] = None  # Required only for COMPLETED status
    title: str
    customer_id: Optional[str] = None
    customer_name: str
    location_type: LocationType = LocationType.ON_SITE
    location: str
    task_category_id: Optional[int] = None
    task_description: Optional[str] = None  # Required only for COMPLETED status
    remarks: Optional[str] = None
    customer_rep: Optional[str] = None
    status: ActivityStatus = ActivityStatus.COMPLETED


class FieldActivityCreate(FieldActivityBase):
    workspace_id: int
    support_staff_id: int

    @model_validator(mode='after')
    def validate_completed_fields(self):
        """Ensure required fields are present when status is COMPLETED"""
        if self.status == ActivityStatus.COMPLETED:
            if not self.start_time:
                raise ValueError("start_time is required for COMPLETED status")
            if not self.end_time:
                raise ValueError("end_time is required for COMPLETED status")
            if not self.task_description:
                raise ValueError("task_description is required for COMPLETED status")
        return self


class FieldActivityUpdate(BaseModel):
    activity_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    title: Optional[str] = None
    customer_id: Optional[str] = None
    customer_name: Optional[str] = None
    location_type: Optional[LocationType] = None
    location: Optional[str] = None
    task_category_id: Optional[int] = None
    task_description: Optional[str] = None
    remarks: Optional[str] = None
    customer_rep: Optional[str] = None
    support_staff_id: Optional[int] = None
    status: Optional[ActivityStatus] = None


class FieldActivityResponse(FieldActivityBase):
    id: int
    workspace_id: int
    support_staff_id: int
    created_by: int
    updated_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    duration_hours: Optional[float] = None  # None for pending tasks

    # Nested objects
    support_staff_name: Optional[str] = None
    created_by_name: Optional[str] = None
    updated_by_name: Optional[str] = None
    task_category: Optional[TaskCategoryResponse] = None

    class Config:
        from_attributes = True


class FieldActivityDetailResponse(FieldActivityResponse):
    photos: List[FieldActivityPhotoResponse] = []

    class Config:
        from_attributes = True
