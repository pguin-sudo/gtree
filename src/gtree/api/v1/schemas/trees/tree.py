from typing import final
from uuid import UUID

from gtree.api.v1.schemas.base import BaseSchema
from gtree.domain.entities._value_objects.tree_access_level import TreeAccessLevel
from gtree.domain.entities.trees.tree import TreeEntity


@final
class TreeCreateRequestSchema(BaseSchema):
    name: str
    description: str


@final
class TreeUpdateRequestSchema(BaseSchema):
    name: str | None
    description: str | None


@final
class TreeResponseSchema(BaseSchema):
    id: UUID
    name: str
    description: str


@final
class TreeFullResponseSchema(BaseSchema): ...
