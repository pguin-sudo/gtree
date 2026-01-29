from dataclasses import dataclass, field

from gtree.domain.entities.base import ObjectBaseEntity
from gtree.domain.exceptions import DomainValidationException


@dataclass(kw_only=True, slots=True)
class TreeEntity(ObjectBaseEntity):
    """Tree entity representing a family tree."""

    name: str
    description: str | None = field(default=None)

    def __post_init__(self):
        if not (1 <= len(self.name) <= 128):
            raise DomainValidationException(
                "Name must be between 1 and 128 characters long"
            )

        if self.description is not None and len(self.description) > 1024:
            raise DomainValidationException(
                "Description must not exceed 1024 characters"
            )

    @classmethod
    def create_tree(
        cls,
        name: str,
        description: str | None = None,
    ) -> "TreeEntity":
        """Create a new tree entity."""
        try:
            return cls(
                name=name,
                description=description,
            )
        except DomainValidationException:
            raise
