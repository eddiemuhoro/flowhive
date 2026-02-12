from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime


class FieldActivityAnalytics(BaseModel):
    total_activities: int
    total_hours: float
    activities_this_week: int
    activities_this_month: int
    top_staff: List[Dict[str, Any]] = []  # Top field staff by activity count
    category_distribution: Dict[str, int] = {}  # Activities by category


class TaskAnalytics(BaseModel):
    total_tasks: int
    completed_tasks: int
    in_progress_tasks: int
    overdue_tasks: int
    completion_rate: float
    average_completion_time: Optional[float] = None  # in days


class ProjectAnalytics(BaseModel):
    project_id: int
    project_name: str
    total_tasks: int
    completed_tasks: int
    completion_rate: float

    class Config:
        from_attributes = True


class UserProductivity(BaseModel):
    user_id: int
    user_name: str
    tasks_assigned: int
    tasks_completed: int
    completion_rate: float
    average_hours_per_task: Optional[float] = None


class WorkspaceAnalytics(BaseModel):
    workspace_id: int
    workspace_name: str
    total_projects: int
    total_tasks: int
    completed_tasks: int
    active_members: int
    completion_rate: float
    projects: List[ProjectAnalytics] = []
    field_activities: Optional[FieldActivityAnalytics] = None  # Field operations data


class ExecutiveDashboard(BaseModel):
    overview: TaskAnalytics
    workspaces: List[WorkspaceAnalytics] = []
    top_performers: List[UserProductivity] = []
    task_completion_trend: List[Dict[str, Any]] = []  # Time series data
    priority_distribution: Dict[str, int] = {}
    status_distribution: Dict[str, int] = {}
