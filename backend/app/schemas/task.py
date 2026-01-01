from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.task import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None
    start_date: Optional[datetime] = None
    estimated_hours: Optional[int] = None
    position: int = 0


class TaskCreate(TaskBase):
    project_id: int
    parent_task_id: Optional[int] = None
    assignee_id: Optional[int] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    start_date: Optional[datetime] = None
    assignee_id: Optional[int] = None
    estimated_hours: Optional[int] = None
    actual_hours: Optional[int] = None
    position: Optional[int] = None


class TaskResponse(TaskBase):
    id: int
    project_id: int
    parent_task_id: Optional[int] = None
    creator_id: int
    assignee_id: Optional[int] = None
    completed_at: Optional[datetime] = None
    actual_hours: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    assignee_name: Optional[str] = None
    creator_name: Optional[str] = None

    class Config:
        from_attributes = True


class SubtaskResponse(BaseModel):
    id: int
    title: str
    status: TaskStatus
    priority: TaskPriority
    assignee_id: Optional[int] = None
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TaskDetailResponse(TaskResponse):
    subtasks: List[SubtaskResponse] = []
    assignee_name: Optional[str] = None
    creator_name: Optional[str] = None
    workspace_id: Optional[int] = None

    class Config:
        from_attributes = True
