from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.orm import mapped_column

from app.core.models.base import Base


class Users(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(nullable=False, unique=True)
