from typing import final
from uuid import UUID

from gtree.api.v1.schemas.base import BaseSchema
from gtree.domain.entities.trees.blood_relation import BloodRelationEntity


@final
class BloodRelationResponseSchema(BaseSchema):
    parent_id: UUID
    child_id: UUID

    @classmethod
    def from_entity(cls, entity: BloodRelationEntity) -> "BloodRelationResponseSchema":
        return BloodRelationResponseSchema(
            parent_id=entity.parent_id,
            child_id=entity.child_id,
        )


class BloodRelationCreateRequestSchema(BaseSchema):
    parent_id: UUID
    child_id: UUID
