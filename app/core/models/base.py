import uuid
from datetime import datetime
from sqlalchemy import MetaData
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.sqltypes import DateTime

from app.core.config import settings


class Base(DeclarativeBase):
    __abstract__ = True
    metadata = MetaData(naming_convention=settings.db.naming_conventions)
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
