import uuid

from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import Text, String

from app.core.models.base import Base
from app.core.models.users import Users


class Projects(Base):
    __tablename__ = "projects"

    project_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    comments: Mapped[str | None] = mapped_column(Text, nullable=True)

    # внешний ключ на пользователя
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    photos:Mapped[list["PhotoProjects"]] = relationship(
        "PhotoProjects",                       # имя класса в кавычках
        back_populates="project",
        cascade="all, delete-orphan",
    )

    # проект принадлежит одному пользователю
    user: Mapped["Users"] = relationship(
        "Users",
        back_populates="projects",
    )

class PhotoProjects(Base):
    __tablename__ = "photo_projects"
    link:Mapped[str] = mapped_column(String(255), nullable=False)
    project_id:Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    project:Mapped["Projects"] = relationship("Projects", back_populates="photos",)