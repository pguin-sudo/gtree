from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field

from gtree.domain.funcs.time import get_current_time


class BaseEntity(BaseModel):
    """Base entity with common fields and methods."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        str_strip_whitespace=True,
        from_attributes=True,
    )
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)
    is_active: bool = Field(default=True)


class ObjectBaseEntity(BaseEntity):
    """Base class for object entities."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4)

    def __hash__(self) -> int:
        return hash(self.id)


class AssociationBaseEntity(BaseEntity):
    """Base class for associative entities.

    Association entities are used to establish relationships between other entities.
    They typically have a foreign key reference to the primary entity and may include additional metadata or attributes.
    """
