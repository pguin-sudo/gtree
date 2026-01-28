from uuid import UUID

from pydantic import Field

from gtree.domain.entities.base import (
    AssociationBaseEntity,
)


class TreeAccessEntity(AssociationBaseEntity):
    """TreeAccess entity representing user access to a tree."""

    user_id: UUID = Field(description="ID of the user")
    tree_id: UUID = Field(description="ID of the tree")
    access_level: str = Field(
        description="Access level (e.g., 'owner', 'editor', 'viewer')",
        pattern=r"^(owner|editor|viewer)$",
    )

    @classmethod
    def create_tree_access(
        cls,
        user_id: UUID,
        tree_id: UUID,
        access_level: str,
    ) -> "TreeAccessEntity":
        """Create a new tree access entity."""
        return TreeAccessEntity(
            user_id=user_id,
            tree_id=tree_id,
            access_level=access_level,
        )
