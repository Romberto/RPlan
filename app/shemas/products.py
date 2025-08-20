from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProjectRead(BaseModel):
    project_name: str
    comments: Optional[str] = None
    user_id: UUID
    photos: list[str] = []

    model_config = ConfigDict(from_attributes=True)


class ProjectReadAll(BaseModel):
    projects: list[ProjectRead]
    total: int
