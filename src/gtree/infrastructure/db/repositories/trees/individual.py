from uuid import UUID

from sqlalchemy import delete, exc, select
from sqlalchemy.ext.asyncio import AsyncSession

from gtree.domain.entities.trees.individual import IndividualEntity
from gtree.infrastructure.db.exceptions import (
    ConflictException,
    NotFoundException,
    RepositoryException,
)
from gtree.infrastructure.db.mappers.individual import IndividualMapper
from gtree.infrastructure.db.models.trees.individual import IndividualModel
from gtree.infrastructure.db.repositories.base import RepositoryObjectBase


class IndividualRepository(RepositoryObjectBase):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def create(self, individual: IndividualEntity) -> IndividualEntity:
        try:
            db_obj = IndividualMapper.entity_to_model(individual)
            self.db.add(db_obj)
            await self.db.flush()
            await self.db.refresh(db_obj)
            return IndividualMapper.model_to_entity(db_obj)
        except exc.SQLAlchemyError as e:
            raise ConflictException(f"Error creating individual: {str(e)}") from e

    async def get_by_tree_id(self, tree_id: UUID) -> list[IndividualEntity]:
        try:
            stmt = select(IndividualModel).where(
                IndividualModel.tree_id == tree_id,
            )
            individuals = await self.db.scalars(stmt)
            return [
                IndividualMapper.model_to_entity(individual)
                for individual in individuals
            ]
        except exc.SQLAlchemyError as e:
            raise RepositoryException(
                f"Error retrieving individuals for tree {tree_id}: {e!s}"
            ) from e

    async def get_by_id(self, individual_id: UUID) -> IndividualEntity:
        try:
            stmt = select(IndividualModel).where(
                IndividualModel.id == individual_id,
            )

            individual = await self.db.scalar(stmt)
            if individual is None:
                raise NotFoundException(f"Individual with id {individual_id} not found")
            return IndividualMapper.model_to_entity(individual)
        except exc.SQLAlchemyError as e:
            raise RepositoryException(
                f"Error retrieving accessible individuals with id {individual_id}: {e!s}"
            ) from e

    async def update(self, individual_entity: IndividualEntity) -> IndividualEntity:
        """Update an existing individual with data from IndividualEntity.

        Raises:
            NotFoundException: If individual with the given ID doesn't exist
            ConflictException: If there's a database error during update
        """
        try:
            stmt = select(IndividualModel).where(
                IndividualModel.id == individual_entity.id
            )
            db_obj = await self.db.scalar(stmt)

            if db_obj is None:
                raise NotFoundException(
                    f"Individual with id {individual_entity.id} not found"
                )

            updated_model = IndividualMapper.entity_to_model(individual_entity)

            for field in IndividualModel.__table__.columns:
                field_name = field.name
                if field_name != "id" and hasattr(updated_model, field_name):
                    new_value = getattr(updated_model, field_name)
                    if new_value is not None:
                        setattr(db_obj, field_name, new_value)

            await self.db.flush()
            await self.db.refresh(db_obj)

            return IndividualMapper.model_to_entity(db_obj)

        except exc.SQLAlchemyError as e:
            raise ConflictException(
                f"Error updating individual with id {individual_entity.id}: {str(e)}"
            ) from e

    async def delete(self, individual_id: UUID) -> None:
        try:
            stmt = delete(IndividualModel).where(IndividualModel.id == individual_id)
            await self.db.execute(stmt)
            await self.db.flush()

        except exc.SQLAlchemyError as e:
            raise ConflictException(
                f"Error deleting individual with id {individual_id}: {str(e)}"
            ) from e
