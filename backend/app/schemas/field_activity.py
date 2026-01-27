from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date, time


# TaskCategory Schemas
class TaskCategoryBase(BaseModel):
    name: str
    title: str
    description: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None


class TaskCategoryCreate(TaskCategoryBase):
    workspace_id: int


class TaskCategoryUpdate(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    is_active: Optional[bool] = None


class TaskCategoryResponse(TaskCategoryBase):
    id: int
    workspace_id: int
    is_active: bool
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
    start_time: time
    end_time: time
    title: str
    customer_name: str
    location: str
    task_category_id: Optional[int] = None
    task_description: str
    remarks: Optional[str] = None
    customer_rep: Optional[str] = None


class FieldActivityCreate(FieldActivityBase):
    workspace_id: int
    support_staff_id: int


class FieldActivityUpdate(BaseModel):
    activity_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    title: Optional[str] = None
    customer_name: Optional[str] = None
    location: Optional[str] = None
    task_category_id: Optional[int] = None
    task_description: Optional[str] = None
    remarks: Optional[str] = None
    customer_rep: Optional[str] = None
    support_staff_id: Optional[int] = None


class FieldActivityResponse(FieldActivityBase):
    id: int
    workspace_id: int
    support_staff_id: int
    created_by: int
    updated_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    duration_hours: float
    
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
