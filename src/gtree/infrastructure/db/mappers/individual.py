from gtree.domain.entities._value_objects.gender import Gender
from gtree.domain.entities.trees.individual import IndividualEntity
from gtree.infrastructure.db.models.trees.individual import IndividualModel


class IndividualMapper:
    @classmethod
    def entity_to_model(cls, entity: IndividualEntity) -> IndividualModel:
        return IndividualModel(
            id=entity.id,
            tree_id=entity.tree_id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            patronymic=entity.patronymic,
            gender=str(entity.gender),
            birth_date=entity.birth_date,
            birth_date_precision=entity.birth_date_precision,
            death_date=entity.death_date,
            death_date_precision=entity.death_date_precision,
            birth_place=entity.birth_place,
            death_place=entity.death_place,
            bio=entity.bio,
            avatar_url=entity.avatar_url,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            is_active=entity.is_active,
        )

    @classmethod
    def model_to_entity(cls, model: IndividualModel) -> IndividualEntity:
        return IndividualEntity(
            id=model.id,
            tree_id=model.tree_id,
            first_name=model.first_name,
            last_name=model.last_name,
            patronymic=model.patronymic,
            gender=Gender.from_string(model.gender),
            birth_date=model.birth_date,
            birth_date_precision=model.birth_date_precision,
            death_date=model.death_date,
            death_date_precision=model.death_date_precision,
            birth_place=model.birth_place,
            death_place=model.death_place,
            bio=model.bio,
            avatar_url=model.avatar_url,
            created_at=model.created_at,
            updated_at=model.updated_at,
            is_active=model.is_active,
        )
