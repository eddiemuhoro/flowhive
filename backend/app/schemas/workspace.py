from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class WorkspaceBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None


class WorkspaceMemberResponse(BaseModel):
    id: int
    user_id: int
    username: str
    email: str
    full_name: Optional[str]
    avatar_url: Optional[str]
    joined_at: datetime

    class Config:
        from_attributes = True


class WorkspaceProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class WorkspaceResponse(WorkspaceBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class WorkspaceDetailResponse(WorkspaceResponse):
    members: List[WorkspaceMemberResponse] = []
    # projects: List[WorkspaceProjectResponse] = []

    class Config:
        from_attributes = True
