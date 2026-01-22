from abc import ABC
from collections.abc import Generator, Sequence
from typing import Any, Generic, TypeVar
from uuid import UUID

from sqlalchemy import asc, desc, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from gtree.domain.entities.base import AssociationBaseEntity, ObjectBaseEntity
from gtree.infrastructure.db.exceptions import (
    ConflictException,
    NotFoundException,
    SaveException,
)
from gtree.infrastructure.db.models.base import AssociationBaseModel, ObjectBaseModel

ObjectModelType = TypeVar("ObjectModelType", bound=ObjectBaseModel)
AssociationModelType = TypeVar("AssociationModelType", bound=AssociationBaseModel)
ObjectEntityType = TypeVar("ObjectEntityType", bound=ObjectBaseEntity)
AssociationEntityType = TypeVar("AssociationEntityType", bound=AssociationBaseEntity)


class RepositoryObjectBase(ABC, Generic[ObjectModelType, ObjectEntityType]):
    def __init__(
        self,
        model: type[ObjectModelType],
        entity: type[ObjectEntityType],
        db: AsyncSession,
    ):
        self.model = model
        self.entity = entity
        self.db = db
        self._safe_attrs = {"id", "created_at", "updated_at"}

    def _to_entity(self, db_obj: ObjectModelType) -> ObjectEntityType:
        return self.entity.model_validate(db_obj)

    def _to_entity_generator(
        self, db_objs: Sequence[ObjectModelType]
    ) -> Generator[ObjectEntityType]:
        return (self._to_entity(db_obj) for db_obj in db_objs)

    async def _commit(self) -> None:
        await self.db.commit()

    async def _get_db_obj(self, id: UUID) -> ObjectModelType | None:
        try:
            stmt = select(self.model).where(self.model.id == id)
            return await self.db.scalar(stmt)
        except SQLAlchemyError as e:
            raise ConflictException(
                f"Error retrieving db obj for {self.model.__name__} with id {id}: {str(e)}"
            ) from e

    async def get(self, id: UUID) -> ObjectEntityType | None:
        try:
            stmt = select(self.model).where(self.model.id == id)
            db_obj = await self.db.scalar(stmt)
            return self._to_entity(db_obj) if db_obj else None
        except SQLAlchemyError as e:
            raise ConflictException(
                f"Error retrieving {self.model.__name__} with id {id}: {str(e)}"
            ) from e

    async def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: dict[str, Any] | None = None,
        order_by: str | None = None,
        descending: bool = False,
    ) -> list[ObjectEntityType]:
        try:
            stmt = select(self.model)
            if filters:
                for field, value in filters.items():
                    if hasattr(self.model, field):
                        column = getattr(self.model, field)
                        stmt = stmt.where(column == value)
            if order_by and hasattr(self.model, order_by):
                field = getattr(self.model, order_by)
                stmt = stmt.order_by(desc(field) if descending else asc(field))
            else:
                stmt = stmt.order_by(desc(self.model.created_at))
            stmt = stmt.offset(skip).limit(limit)
            result = await self.db.scalars(stmt)
            db_objs = result.all()
            return list(self._to_entity_generator(db_objs))
        except SQLAlchemyError as e:
            raise ConflictException(
                f"Error retrieving multiple {self.model.__name__}: {str(e)}"
            ) from e

    async def create(
        self, *, create_data: dict[str, Any], skip_commit: bool = False
    ) -> ObjectEntityType:
        try:
            db_obj = self.model(**create_data)
            self.db.add(db_obj)
            if not skip_commit:
                await self.db.commit()
                await self.db.refresh(db_obj)
                return self._to_entity(db_obj)
            # When skip_commit=True, flush to populate auto-generated fields
            await self.db.flush()
            return self._to_entity(db_obj)
        except IntegrityError as e:
            if not skip_commit:
                await self.db.rollback()
            raise SaveException(
                f"{self.model.__name__} with provided data already exists: {str(e)}"
            ) from e
        except SQLAlchemyError as e:
            if not skip_commit:
                await self.db.rollback()
            raise SaveException(
                f"Error creating {self.model.__name__}: {str(e)}"
            ) from e

    async def update(
        self,
        *,
        db_obj: ObjectModelType,
        update_data: dict[str, Any],
        skip_commit: bool = False,
    ) -> ObjectEntityType:
        try:
            safe_update_data = {
                k: v
                for k, v in update_data.items()
                if k not in self._safe_attrs and hasattr(db_obj, k)
            }
            for field, value in safe_update_data.items():
                setattr(db_obj, field, value)
            self.db.add(db_obj)
            if not skip_commit:
                await self.db.commit()
                await self.db.refresh(db_obj)
            return self._to_entity(db_obj)
        except IntegrityError as e:
            if not skip_commit:
                await self.db.rollback()
            raise SaveException(
                f"Update would create duplicate {self.model.__name__}: {str(e)}"
            ) from e
        except SQLAlchemyError as e:
            if not skip_commit:
                await self.db.rollback()
            raise SaveException(
                f"Error updating {self.model.__name__}: {str(e)}"
            ) from e

    async def delete(self, *, id: Any, skip_commit: bool = False) -> ObjectEntityType:
        try:
            stmt = select(self.model).where(self.model.id == id)
            db_obj = await self.db.scalar(stmt)
            if not db_obj:
                raise NotFoundException(f"{self.model.__name__} with id {id} not found")
            await self.db.delete(db_obj)
            if not skip_commit:
                await self.db.commit()
            return self._to_entity(db_obj)
        except NotFoundException:
            raise
        except SQLAlchemyError as e:
            if not skip_commit:
                await self.db.rollback()
            raise ConflictException(
                f"Error deleting {self.model.__name__} with id {id}: {str(e)}"
            ) from e


class RepositoryAssociationBase(
    ABC, Generic[AssociationModelType, AssociationEntityType]
):
    def __init__(
        self,
        model: type[AssociationModelType],
        entity: type[AssociationEntityType],
        db: AsyncSession,
    ):
        self.model = model
        self.entity = entity
        self.db = db
        self._safe_attrs = {"created_at", "updated_at"}

    def _to_entity(self, db_obj: AssociationModelType) -> AssociationEntityType:
        data = {}
        for column in db_obj.__table__.columns:
            data[column.name] = getattr(db_obj, column.name)

        # Convert relationships if needed
        # Example for a single relationship:
        # if db_obj.some_relationship:
        #     data['some_relationship'] = self._to_entity(db_obj.some_relationship)

        return self.entity(**data)

    def _to_entity_generator(
        self, db_objs: Sequence[AssociationModelType]
    ) -> Generator[AssociationEntityType]:
        return (self._to_entity(db_obj) for db_obj in db_objs)

    async def commit(self) -> None:
        await self.db.commit()

    async def get(self, filters: dict[str, Any]) -> AssociationEntityType | None:
        try:
            stmt = select(self.model)
            for field, value in filters.items():
                if hasattr(self.model, field):
                    column = getattr(self.model, field)
                    stmt = stmt.where(column == value)
            db_obj = await self.db.scalar(stmt)
            return self._to_entity(db_obj) if db_obj else None
        except SQLAlchemyError as e:
            raise ConflictException(
                f"Error retrieving {self.model.__name__} with filters {filters}: {str(e)}"
            ) from e

    async def get_db_obj(self, filters: dict[str, Any]) -> AssociationModelType | None:
        try:
            stmt = select(self.model)
            for field, value in filters.items():
                if hasattr(self.model, field):
                    column = getattr(self.model, field)
                    stmt = stmt.where(column == value)
            return await self.db.scalar(stmt)
        except SQLAlchemyError as e:
            raise ConflictException(
                f"Error retrieving db obj for {self.model.__name__} with filters {filters}: {str(e)}"
            ) from e

    async def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: dict[str, Any] | None = None,
        order_by: str | None = None,
        descending: bool = False,
    ) -> list[AssociationEntityType]:
        try:
            stmt = select(self.model)
            if filters:
                for field, value in filters.items():
                    if hasattr(self.model, field):
                        column = getattr(self.model, field)
                        stmt = stmt.where(column == value)
            if order_by and hasattr(self.model, order_by):
                field = getattr(self.model, order_by)
                stmt = stmt.order_by(desc(field) if descending else asc(field))
            else:
                stmt = stmt.order_by(desc(self.model.created_at))
            stmt = stmt.offset(skip).limit(limit)
            result = await self.db.scalars(stmt)
            db_objs = result.all()
            return list(self._to_entity_generator(db_objs))
        except SQLAlchemyError as e:
            raise ConflictException(
                f"Error retrieving multiple {self.model.__name__}: {str(e)}"
            ) from e

    async def create(
        self, *, create_data: dict[str, Any], skip_commit: bool = False
    ) -> AssociationEntityType:
        try:
            db_obj = self.model(**create_data)
            self.db.add(db_obj)
            if not skip_commit:
                await self.db.commit()
                await self.db.refresh(db_obj)
                return self._to_entity(db_obj)
            # When skip_commit=True, flush to populate auto-generated fields
            await self.db.flush()
            return self._to_entity(db_obj)
        except IntegrityError as e:
            if not skip_commit:
                await self.db.rollback()
            raise SaveException(
                f"{self.model.__name__} with provided data already exists: {str(e)}"
            ) from e
        except SQLAlchemyError as e:
            if not skip_commit:
                await self.db.rollback()
            raise SaveException(
                f"Error creating {self.model.__name__}: {str(e)}"
            ) from e

    async def update(
        self,
        *,
        db_obj: AssociationModelType,
        update_data: dict[str, Any],
        skip_commit: bool = False,
    ) -> AssociationEntityType:
        try:
            safe_update_data = {
                k: v
                for k, v in update_data.items()
                if k not in self._safe_attrs and hasattr(db_obj, k)
            }
            for field, value in safe_update_data.items():
                setattr(db_obj, field, value)
            self.db.add(db_obj)
            if not skip_commit:
                await self.db.commit()
                await self.db.refresh(db_obj)
            return self._to_entity(db_obj)
        except IntegrityError as e:
            if not skip_commit:
                await self.db.rollback()
            raise SaveException(
                f"Update would create duplicate {self.model.__name__}: {str(e)}"
            ) from e
        except SQLAlchemyError as e:
            if not skip_commit:
                await self.db.rollback()
            raise SaveException(
                f"Error updating {self.model.__name__}: {str(e)}"
            ) from e

    async def delete(
        self, filters: dict[str, Any], skip_commit: bool = False
    ) -> AssociationEntityType:
        try:
            db_obj = await self.get_db_obj(filters)
            if not db_obj:
                raise NotFoundException(
                    f"{self.model.__name__} with filters {filters} not found"
                )
            await self.db.delete(db_obj)
            if not skip_commit:
                await self.db.commit()
            return self._to_entity(db_obj)
        except NotFoundException:
            raise
        except SQLAlchemyError as e:
            if not skip_commit:
                await self.db.rollback()
            raise ConflictException(
                f"Error deleting {self.model.__name__} with filters {filters}: {str(e)}"
            ) from e
