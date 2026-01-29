from gtree.domain.entities.trees.tree_access import TreeAccessEntity
from gtree.infrastructure.db.models.trees.tree_access import TreeAccessModel


class TreeAccessMapper:
    @classmethod
    def entity_to_model(cls, entity: TreeAccessEntity) -> TreeAccessModel:
        return TreeAccessModel(
            user_id=entity.user_id,
            tree_id=entity.tree_id,
            access_level=entity.access_level,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            is_active=entity.is_active,
        )

    @classmethod
    def model_to_entity(cls, model: TreeAccessModel) -> TreeAccessEntity:
        return TreeAccessEntity(
            user_id=model.user_id,
            tree_id=model.tree_id,
            access_level=model.access_level,
            created_at=model.created_at,
            updated_at=model.updated_at,
            is_active=model.is_active,
        )
