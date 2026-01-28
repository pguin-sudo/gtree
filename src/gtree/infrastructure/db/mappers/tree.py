from gtree.domain.entities.trees.tree import TreeEntity
from gtree.infrastructure.db.models.trees.tree import TreeModel


class TreeMapper:
    @classmethod
    def entity_to_model(cls, entity: TreeEntity) -> TreeModel:
        return TreeModel(id=entity.id, name=entity.name, description=entity.description)

    @classmethod
    def model_to_entity(cls, entity: TreeModel) -> TreeEntity:
        return TreeEntity.model_validate(entity)
