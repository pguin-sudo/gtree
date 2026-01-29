from dataclasses import dataclass
from uuid import UUID

from gtree.domain.entities._value_objects.tree_access_level import TreeAccessLevel
from gtree.domain.entities.base import AssociationBaseEntity
from gtree.domain.exceptions import DomainValidationException


@dataclass(kw_only=True, slots=True)
class TreeAccessEntity(AssociationBaseEntity):
    """TreeAccess entity representing user access to a tree."""

    user_id: UUID
    tree_id: UUID
    access_level: TreeAccessLevel

    def __post_init__(self) -> None:
        """Validate the entity after initialization."""
        if isinstance(self.access_level, str):
            self.access_level = TreeAccessLevel.from_string(self.access_level)

    @classmethod
    def create_tree_access(
        cls,
        user_id: UUID,
        tree_id: UUID,
        access_level: str,
    ) -> "TreeAccessEntity":
        """Create a new tree access entity with validation."""
        try:
            return cls(
                user_id=user_id,
                tree_id=tree_id,
                access_level=access_level,
            )
        except DomainValidationException:
            raise

    def __str__(self) -> str:
        return f"TreeAccess(user={self.user_id}, tree={self.tree_id}, level={self.access_level})"
