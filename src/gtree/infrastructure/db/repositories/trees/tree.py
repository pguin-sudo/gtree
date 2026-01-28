from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from gtree.domain.entities._value_objects.tree_access_level import TreeAccessLevel
from gtree.domain.entities.trees.tree import TreeEntity
from gtree.infrastructure.db.exceptions import ConflictException
from gtree.infrastructure.db.mappers.tree import TreeMapper
from gtree.infrastructure.db.models.trees.tree import TreeModel
from gtree.infrastructure.db.models.trees.tree_access import TreeAccessModel
from gtree.infrastructure.db.repositories.base import RepositoryObjectBase


class TreeRepository(RepositoryObjectBase):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def create(self, tree: TreeEntity) -> TreeEntity:
        try:
            db_obj = TreeMapper.entity_to_model(tree)
            self.db.add(db_obj)
            await self.db.commit()
            await self.db.refresh(db_obj)
            return TreeMapper.model_to_entity(db_obj)
        except SQLAlchemyError as e:
            raise ConflictException(f"Error creating tree: {str(e)}") from e

    async def get_accessible_trees(
        self, user_id: UUID4, access_level: TreeAccessLevel
    ) -> list[TreeEntity]:
        try:
            stmt = (
                select(TreeModel, TreeAccessModel)
                .distinct(TreeModel.id)
                .join(TreeAccessModel, TreeModel.id == TreeAccessModel.tree_id)
                .where(
                    TreeAccessModel.user_id == user_id,
                    TreeAccessModel.access_level == access_level,
                )
            )
            result = await self.db.scalars(stmt)
            return [TreeMapper.model_to_entity(tree) for tree in result.all()]
        except SQLAlchemyError as e:
            raise ConflictException(
                f"Error retrieving accessible trees for user {user_id}: {e!s}"
            ) from e
