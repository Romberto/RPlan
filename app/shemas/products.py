from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PhotoRead(BaseModel):
    id: UUID
    link: str
    project_id: UUID

    model_config = ConfigDict(from_attributes=True)


class ProjectRead(BaseModel):
    id: UUID
    project_name: str
    created_at: datetime
    comments: Optional[str] = None
    user_id: UUID
    photos: list[PhotoRead] = []

    model_config = ConfigDict(from_attributes=True)


class ProjectCreate(BaseModel):
    project_name: str
    comments: Optional[str] = None
    photos: Optional[list[PhotoRead]] = []

class ProjectUpdate(BaseModel):
    project_name: Optional[str]
    comments: Optional[str]
    photos: Optional[list[PhotoRead]]


class ProjectReadAll(BaseModel):
    projects: list[ProjectRead] = []
    total: int
