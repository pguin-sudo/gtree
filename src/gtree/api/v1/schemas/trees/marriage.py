from datetime import date
from typing import final
from uuid import UUID

from gtree.api.v1.schemas.base import BaseSchema
from gtree.domain.entities._value_objects.gender import Gender
from gtree.domain.entities.trees.individual import IndividualEntity


# TODO1
@final
class IndividualResponseSchema(BaseSchema):
    id: UUID
    tree_id: UUID
    first_name: str
    last_name: str | None
    patronymic: str | None
    gender: Gender
    birth_date: date | None
    birth_date_precision: str | None
    death_date: date | None
    death_date_precision: str | None
    birth_place: str | None
    death_place: str | None
    bio: str | None
    avatar_url: str | None

    @classmethod
    def from_entity(cls, entity: IndividualEntity) -> "IndividualResponseSchema":
        return IndividualResponseSchema(
            id=entity.id,
            tree_id=entity.tree_id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            patronymic=entity.patronymic,
            gender=entity.gender,
            birth_date=entity.birth_date,
            birth_date_precision=entity.birth_date_precision,
            death_date=entity.death_date,
            death_date_precision=entity.death_date_precision,
            birth_place=entity.birth_place,
            death_place=entity.death_place,
            bio=entity.bio,
            avatar_url=entity.avatar_url,
        )


class IndividualCreateRequestSchema(BaseSchema):
    first_name: str
    last_name: str | None
    patronymic: str | None
    gender: Gender
    birth_date: date | None
    birth_date_precision: str | None
    death_date: date | None
    death_date_precision: str | None
    birth_place: str | None
    death_place: str | None
    bio: str | None
    avatar_url: str | None


class IndividualUpdateRequestSchema(BaseSchema):
    first_name: str | None = None
    last_name: str | None = None
    patronymic: str | None = None
    gender: Gender | None = None
    birth_date: date | None = None
    birth_date_precision: str | None = None
    death_date: date | None = None
    death_date_precision: str | None = None
    birth_place: str | None = None
    death_place: str | None = None
    bio: str | None = None
    avatar_url: str | None = None
