from datetime import UTC, datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field


class BaseEntity(BaseModel):
    """Base entity with common fields and methods."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        revalidate_instances="always",
        str_strip_whitespace=True,
        from_attributes=True,
    )


class ObjectBaseEntity(BaseEntity):
    """Base class for object entities."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    is_active: bool = Field(default=True)


class AssociationBaseEntity(BaseEntity):
    """Base class for associative entities.

    Association entities are used to establish relationships between other entities.
    They typically have a foreign key reference to the primary entity and may include additional metadata or attributes.
    """

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    is_active: bool = Field(default=True)
