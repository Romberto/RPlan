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


class ProjectReadAll(BaseModel):
    projects: list[ProjectRead]=[]
    total: int
