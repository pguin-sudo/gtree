from gtree.domain.entities.trees.tree_access import TreeAccessEntity
from gtree.infrastructure.db.models.trees.tree_access import TreeAccessModel


class TreeAccessMapper:
    @classmethod
    def entity_to_model(cls, entity: TreeAccessEntity) -> TreeAccessModel:
        return TreeAccessModel(
            user_id=entity.user_id,
            tree_id=entity.tree_id,
            access_level=entity.access_level,
        )

    @classmethod
    def model_to_entity(cls, entity: TreeAccessModel) -> TreeAccessEntity:
        return TreeAccessEntity.model_validate(entity)
