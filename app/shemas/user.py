from datetime import datetime
from enum import Enum

from pydantic import BaseModel, constr


class Role(str, Enum):
    user = "user"
    admin = "admin"


class UserRead(BaseModel):
    id: str
    username: constr(min_length=4, max_length=255)
    created_at: datetime
    role: str
