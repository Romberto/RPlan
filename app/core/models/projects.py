from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.orm import mapped_column
from app.core.models.base import Base


class Projects(Base):
    __tablename__ = "projects"
    project_name: Mapped[str] = mapped_column(nullable=False, unique=True)


class PhotoProjects(Base):
    __tablename__ = "photo_projects"
