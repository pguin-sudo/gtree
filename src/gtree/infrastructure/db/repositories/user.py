from sqlalchemy import exists, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from gtree.domain.entities.user import UserEntity
from gtree.infrastructure.db.exceptions import ConflictException, NotFoundException
from gtree.infrastructure.db.mappers.user import UserMapper
from gtree.infrastructure.db.models.user import UserModel
from gtree.infrastructure.db.repositories.base import RepositoryObjectBase


class UserRepository(RepositoryObjectBase):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def create(self, user: UserEntity) -> UserEntity:
        try:
            db_obj = UserMapper.entity_to_model(user)
            self.db.add(db_obj)
            await self.db.commit()
            await self.db.refresh(db_obj)
            return UserMapper.model_to_entity(db_obj)
        except SQLAlchemyError as e:
            raise ConflictException(f"Error creating user: {str(e)}") from e

    async def get_by_id(self, user_id) -> UserEntity:
        try:
            stmt = select(UserModel).where(UserModel.id == user_id)
            db_obj = await self.db.scalar(stmt)
            if not db_obj:
                raise NotFoundException(f"User with id {user_id} not found")
            return UserMapper.model_to_entity(db_obj)
        except SQLAlchemyError as e:
            raise ConflictException(
                f"Error retrieving user by id {id}: {str(e)}"
            ) from e

    async def get_by_email(self, email: str) -> UserEntity | None:
        """Get user by email address."""
        try:
            stmt = select(UserModel).where(UserModel.email == email)
            db_obj = await self.db.scalar(stmt)
            if db_obj is None:
                return None
            return UserMapper.model_to_entity(db_obj)
        except SQLAlchemyError as e:
            raise ConflictException(
                f"Error retrieving user by email {email}: {str(e)}"
            ) from e

    async def get_by_username(self, username: str) -> UserEntity | None:
        """Get user by username."""
        try:
            stmt = select(UserModel).where(UserModel.username == username)
            db_obj = await self.db.scalar(stmt)
            if db_obj is None:
                return None
            return UserMapper.model_to_entity(db_obj)
        except SQLAlchemyError as e:
            raise ConflictException(
                f"Error retrieving user by username {username}: {str(e)}"
            ) from e

    async def exists_by_email(self, email: str) -> bool:
        """Check if a user with the given email exists."""
        try:
            stmt = select(exists().where(UserModel.email == email))
            result = await self.db.scalar(stmt)
            return False if result is None else result
        except SQLAlchemyError as e:
            raise ConflictException(f"Error checking email existence: {str(e)}") from e

    async def update(self, user_entity: UserEntity) -> UserEntity:
        """Update an existing user with data from UserEntity.

        Args:
            user_entity: The UserEntity containing updated data

        Returns:
            The updated UserEntity

        Raises:
            NotFoundException: If user with the given ID doesn't exist
            ConflictException: If there's a database error during update
        """
        try:
            stmt = select(UserModel).where(UserModel.id == user_entity.id)
            db_obj = await self.db.scalar(stmt)

            if not db_obj:
                raise NotFoundException(f"User with id {user_entity.id} not found")

            updated_model = UserMapper.entity_to_model(user_entity)

            for field in UserModel.__table__.columns:
                field_name = field.name
                if field_name != "id" and hasattr(updated_model, field_name):
                    new_value = getattr(updated_model, field_name)
                    if new_value is not None:
                        setattr(db_obj, field_name, new_value)

            await self.db.commit()
            await self.db.refresh(db_obj)

            return UserMapper.model_to_entity(db_obj)

        except SQLAlchemyError as e:
            await self.db.rollback()
            raise ConflictException(
                f"Error updating user with id {user_entity.id}: {str(e)}"
            ) from e
