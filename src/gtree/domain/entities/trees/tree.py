from pydantic import Field

from gtree.domain.entities.base import (
    ObjectBaseEntity,
)


class TreeEntity(ObjectBaseEntity):
    """Tree entity representing a family tree."""

    name: str = Field(
        min_length=1,
        max_length=128,
        description="Name of the family tree",
    )
    description: str | None = Field(
        default=None,
        max_length=1024,
        description="Optional description of the tree",
    )

    @classmethod
    def create_tree(
        cls,
        name: str,
        description: str | None = None,
    ) -> "TreeEntity":
        """Create a new tree entity."""
        return TreeEntity(
            name=name,
            description=description,
        )
