from uuid import UUID

from sqlalchemy import exc, exists, select
from sqlalchemy.dialects.postgresql import insert
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

    async def upsert(self, user: TreeAccessEntity) -> TreeAccessEntity:
        try:
            db_obj = TreeAccessMapper.entity_to_model(user)

            stmt = (
                insert(TreeAccessModel)
                .values(
                    user_id=db_obj.user_id,
                    tree_id=db_obj.tree_id,
                    access_level=db_obj.access_level,
                )
                .on_conflict_do_update(
                    index_elements=["user_id", "tree_id"],
                    set_={"access_level": db_obj.access_level},
                )
                .returning(TreeAccessModel)
            )

            result = await self.db.execute(stmt)
            updated_obj = result.scalar_one()
            await self.db.commit()

            return TreeAccessMapper.model_to_entity(updated_obj)
        except exc.SQLAlchemyError as e:
            await self.db.rollback()
            raise ConflictException(f"Error creating tree access: {str(e)}") from e

    async def has_exact_access_level(
        self, tree_id: UUID, user_id: UUID, access_level: TreeAccessLevel
    ) -> bool:
        """Checks if the user has the exact access level."""
        try:
            stmt = select(
                exists().where(
                    TreeAccessModel.tree_id == tree_id,
                    TreeAccessModel.user_id == user_id,
                    TreeAccessModel.access_level == access_level,
                )
            )
            result = await self.db.scalar(stmt)
            return bool(result)
        except exc.SQLAlchemyError as e:
            raise RepositoryException(
                f"Error checking exact tree access: {str(e)}"
            ) from e

    async def has_minimum_access_level(
        self, tree_id: UUID, user_id: UUID, min_access_level: TreeAccessLevel
    ) -> bool:
        """Checks if the user has at least the specified minimum access level."""
        try:
            stmt = select(TreeAccessModel.access_level).where(
                TreeAccessModel.tree_id == tree_id, TreeAccessModel.user_id == user_id
            )
            user_access_level = await self.db.scalar(stmt)

            user_level = TreeAccessLevel.from_string(user_access_level)
            return user_level >= min_access_level

        except exc.SQLAlchemyError as e:
            raise RepositoryException(
                f"Error checking minimum tree access: {str(e)}"
            ) from e
