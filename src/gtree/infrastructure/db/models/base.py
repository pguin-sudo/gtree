from datetime import UTC, datetime
from typing import Annotated
import uuid

from sqlalchemy import Boolean, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    """Base class for all models with common fields and methods."""

    __abstract__ = True

    @classmethod
    def from_entity(cls, entity):
        raise NotImplementedError("Subclasses must implement this method")


class ObjectBaseModel(BaseModel):
    """Base class for all models with common fields and methods."""

    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=lambda: uuid.uuid4(), index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=text("TIMEZONE('utc', now())"), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=lambda: datetime.now(UTC).replace(tzinfo=None),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class AssociationBaseModel(BaseModel):
    """Base class for all associative moModeldels with composite PK."""

    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=text("TIMEZONE('utc', now())"), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=lambda: datetime.now(UTC).replace(tzinfo=None),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


uuid_pk = Annotated[
    uuid.UUID,
    mapped_column(
        UUID(as_uuid=True),
        default=lambda: uuid.uuid4(),
        primary_key=True,
        nullable=False,
    ),
]
