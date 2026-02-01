from typing import final
from uuid import UUID

from gtree.api.v1.schemas.base import BaseSchema
from gtree.domain.entities.trees.tree import TreeEntity


@final
class TreeCreateRequestSchema(BaseSchema):
    name: str
    description: str | None = None


@final
class TreeUpdateRequestSchema(BaseSchema):
    name: str | None = None
    description: str | None = None


@final
class TreeResponseSchema(BaseSchema):
    id: UUID
    name: str
    description: str | None = None

    @classmethod
    def from_entity(cls, entity: TreeEntity) -> "TreeResponseSchema":
        return TreeResponseSchema(
            id=entity.id,
            name=entity.name,
            description=entity.description,
        )
