from pydantic import BaseModel
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.schemas.task import TaskResponse


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None


#pass project base to be inherited
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
    tasks: List['TaskResponse'] = []

    class Config:
        from_attributes = True


# Resolve forward references
from app.schemas.task import TaskResponse
ProjectDetailResponse.model_rebuild()
