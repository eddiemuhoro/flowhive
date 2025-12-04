from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TaskListBase(BaseModel):
    name: str
    description: Optional[str] = None
    position: int = 0


class TaskListCreate(TaskListBase):
    project_id: int


class TaskListUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    position: Optional[int] = None


class TaskListResponse(TaskListBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None


class ProjectCreate(ProjectBase):
    workspace_id: int


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None


class ProjectResponse(ProjectBase):
    id: int
    workspace_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectDetailResponse(ProjectResponse):
    task_lists: List[TaskListResponse] = []

    class Config:
        from_attributes = True
