from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql.sqltypes import String

from app.core.models.base import Base
from app.shemas.user import Role


class Users(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    role: Mapped[str] = mapped_column(default=Role.user)

    # один пользователь -> много проектов
    projects: Mapped[list["Projects"]] = relationship(
        "Projects",  # имя класса в кавычках
        back_populates="user",
        cascade="all, delete-orphan",
    )
