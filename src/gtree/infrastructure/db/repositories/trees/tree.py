from uuid import UUID

from sqlalchemy import exc, select
from sqlalchemy.ext.asyncio import AsyncSession

from gtree.domain.entities._value_objects.tree_access_level import TreeAccessLevel
from gtree.domain.entities.trees.tree import TreeEntity
from gtree.infrastructure.db.exceptions import (
    ConflictException,
    NotFoundException,
    RepositoryException,
)
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
            await self.db.flush()
            await self.db.refresh(db_obj)
            return TreeMapper.model_to_entity(db_obj)
        except exc.SQLAlchemyError as e:
            raise ConflictException(f"Error creating tree: {str(e)}") from e

    async def get_accessible_trees(
        self, user_id: UUID, access_level: TreeAccessLevel
    ) -> list[TreeEntity]:
        try:
            stmt = (
                select(TreeModel)
                .distinct(TreeModel.id)
                .join(TreeAccessModel, TreeModel.id == TreeAccessModel.tree_id)
                .where(
                    TreeAccessModel.user_id == user_id,
                    TreeAccessModel.access_level == access_level,
                )
            )
            result = await self.db.scalars(stmt)
            return [TreeMapper.model_to_entity(tree) for tree in result.all()]
        except exc.SQLAlchemyError as e:
            raise RepositoryException(
                f"Error retrieving accessible trees for user {user_id}: {e!s}"
            ) from e

    async def get_by_id(self, tree_id: UUID) -> TreeEntity:
        try:
            stmt = select(TreeModel).where(
                TreeModel.id == tree_id,
            )
            tree = await self.db.scalar(stmt)
            return TreeMapper.model_to_entity(tree)
        except exc.SQLAlchemyError as e:
            raise RepositoryException(
                f"Error retrieving accessible trees with id {tree_id}: {e!s}"
            ) from e

    async def update(self, tree_entity: TreeEntity) -> TreeEntity:
        """Update an existing tree with data from TreeEntity.

        Raises:
            NotFoundException: If tree with the given ID doesn't exist
            ConflictException: If there's a database error during update
        """
        try:
            stmt = select(TreeModel).where(TreeModel.id == tree_entity.id)
            db_obj = await self.db.scalar(stmt)

            if not db_obj:
                raise NotFoundException(f"Tree with id {tree_entity.id} not found")

            updated_model = TreeMapper.entity_to_model(tree_entity)

            for field in TreeModel.__table__.columns:
                field_name = field.name
                if field_name != "id" and hasattr(updated_model, field_name):
                    new_value = getattr(updated_model, field_name)
                    if new_value is not None:
                        setattr(db_obj, field_name, new_value)

            await self.db.flush()
            await self.db.refresh(db_obj)

            return TreeMapper.model_to_entity(db_obj)

        except exc.SQLAlchemyError as e:
            raise ConflictException(
                f"Error updating tree with id {tree_entity.id}: {str(e)}"
            ) from e
