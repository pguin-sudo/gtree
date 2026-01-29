from uuid import UUID

from sqlalchemy import exc, exists, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from gtree.domain.entities._value_objects.tree_access_level import TreeAccessLevel
from gtree.domain.entities.trees.tree_access import TreeAccessEntity
from gtree.infrastructure.db.exceptions import ConflictException, RepositoryException
from gtree.infrastructure.db.mappers.tree_access import TreeAccessMapper
from gtree.infrastructure.db.models.trees.tree_access import TreeAccessModel
from gtree.infrastructure.db.repositories.base import RepositoryObjectBase


class TreeAccessRepository(RepositoryObjectBase):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def create(self, user: TreeAccessEntity) -> TreeAccessEntity:
        try:
            db_obj = TreeAccessMapper.entity_to_model(user)
            self.db.add(db_obj)
            await self.db.flush()
            await self.db.refresh(db_obj)
            return TreeAccessMapper.model_to_entity(db_obj)
        except exc.SQLAlchemyError as e:
            raise ConflictException(f"Error creating tree access: {str(e)}") from e

    async def has_access_to_tree(
        self, tree_id: UUID, user_id: UUID, tree_access_level: TreeAccessLevel
    ) -> bool:
        try:
            stmt = select(
                exists()
                .where(TreeAccessModel.tree_id == tree_id)
                .where(TreeAccessModel.user_id == user_id)
                .where(TreeAccessModel.access_level == tree_access_level)
            )
            result = await self.db.scalar(stmt)
            return False if result is None else result
        except exc.SQLAlchemyError as e:
            raise RepositoryException(f"Error checking tree access: {str(e)}") from e
