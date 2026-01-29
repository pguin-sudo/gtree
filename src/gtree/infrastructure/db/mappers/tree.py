from gtree.domain.entities.trees.tree import TreeEntity
from gtree.infrastructure.db.models.trees.tree import TreeModel


class TreeMapper:
    @classmethod
    def entity_to_model(cls, entity: TreeEntity) -> TreeModel:
        return TreeModel(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            is_active=entity.is_active,
        )

    @classmethod
    def model_to_entity(cls, model: TreeModel) -> TreeEntity:
        return TreeEntity(
            id=model.id,
            name=model.name,
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at,
            is_active=model.is_active,
        )
