from dataclasses import dataclass, field
from datetime import datetime
import uuid

from gtree.domain.funcs.time import get_current_time


@dataclass(kw_only=True, slots=True)
class BaseEntity:
    """Base entity with common fields and methods."""

    created_at: datetime = field(default_factory=get_current_time)
    updated_at: datetime = field(default_factory=get_current_time)
    is_active: bool = field(default=True)


@dataclass(kw_only=True, slots=True)
class ObjectBaseEntity(BaseEntity):
    """Base class for object entities."""

    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass(kw_only=True, slots=True)
class AssociationBaseEntity(BaseEntity):
    """Base class for associative entities.

    Association entities are used to establish relationships between other entities.
    They typically have a foreign key reference to the primary entity and may include additional metadata or attributes.
    """
