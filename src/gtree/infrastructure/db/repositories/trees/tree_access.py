from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio.session import AsyncSession

from gtree.domain.entities.trees.tree_access import TreeAccessEntity
from gtree.infrastructure.db.exceptions import ConflictException
from gtree.infrastructure.db.mappers.tree_access import TreeAccessMapper
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
        except SQLAlchemyError as e:
            raise ConflictException(f"Error creating tree access: {str(e)}") from e
