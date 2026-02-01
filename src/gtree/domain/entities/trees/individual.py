from dataclasses import dataclass
from datetime import date

from sqlalchemy.dialects.postgresql.base import UUID

from gtree.domain.entities._value_objects.gender import Gender
from gtree.domain.entities.base import ObjectBaseEntity
from gtree.domain.exceptions import DomainValidationException


@dataclass(kw_only=True, slots=True)
class IndividualEntity(ObjectBaseEntity):
    tree_id: UUID

    first_name: str
    last_name: str | None
    patronymic: str | None
    gender: Gender | None

    birth_date: date | None
    birth_date_precision: str | None
    death_date: date | None
    death_date_precision: str | None

    birth_place: str | None
    death_place: str | None
    bio: str | None

    avatar_url: str

    def __post_init__(self):
        if not (1 <= len(self.first_name) <= 128):
            raise DomainValidationException(
                "Name must be between 1 and 128 characters long"
            )
        if self.last_name is not None and len(self.last_name) > 128:
            raise DomainValidationException("Last name must not exceed 128 characters")
        if (
            self.birth_date is not None
            and self.death_date is not None
            and self.birth_date > self.death_date
        ):
            raise DomainValidationException("Birth date must be before death date")
        if isinstance(self.gender, str):
            self.gender = Gender.from_string(self.gender)

    @classmethod
    def create_individual(
        cls,
        tree_id: UUID,
        first_name: str,
        gender: Gender,
        last_name: str | None = None,
        patronymic: str | None = None,
        birth_date: date | None = None,
        birth_date_precision: str | None = None,
        death_date: date | None = None,
        death_date_precision: str | None = None,
        birth_place: str | None = None,
        death_place: str | None = None,
        bio: str | None = None,
        avatar_url: str | None = None,
    ) -> "IndividualEntity":
        try:
            return cls(
                tree_id=tree_id,
                first_name=first_name,
                last_name=last_name,
                patronymic=patronymic,
                gender=gender,
                birth_date=birth_date,
                birth_date_precision=birth_date_precision,
                death_date=death_date,
                death_date_precision=death_date_precision,
                birth_place=birth_place,
                death_place=death_place,
                bio=bio,
                avatar_url=avatar_url,
            )
        except DomainValidationException:
            raise

    def update_individual(
        self,
        first_name: str | None = None,
        gender: Gender | None = None,
        last_name: str | None = None,
        patronymic: str | None = None,
        birth_date: date | None = None,
        birth_date_precision: str | None = None,
        death_date: date | None = None,
        death_date_precision: str | None = None,
        birth_place: str | None = None,
        death_place: str | None = None,
        bio: str | None = None,
        avatar_url: str | None = None,
    ) -> None:
        self.first_name = first_name or self.first_name
        self.gender = gender or self.gender
        self.last_name = last_name or self.last_name
        self.patronymic = patronymic or self.patronymic
        self.birth_date = birth_date or self.birth_date
        self.birth_date_precision = birth_date_precision or self.birth_date_precision
        self.death_date = death_date or self.death_date
        self.death_date_precision = death_date_precision or self.death_date_precision
        self.birth_place = birth_place or self.birth_place
        self.death_place = death_place or self.death_place
        self.bio = bio or self.bio
        self.avatar_url = avatar_url or self.avatar_url
        self.__post_init__()
