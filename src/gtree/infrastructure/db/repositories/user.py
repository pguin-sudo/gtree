from datetime import UTC, datetime

from pydantic import UUID4
from sqlalchemy import exists, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from gtree.domain.entities.user import UserEntity
from gtree.infrastructure.db.exceptions import ConflictException, NotFoundException
from gtree.infrastructure.db.models.user import UserModel
from gtree.infrastructure.db.repositories.base import RepositoryObjectBase


class UserRepository(RepositoryObjectBase[UserModel, UserEntity]):
    def __init__(self, db: AsyncSession):
        super().__init__(UserModel, UserEntity, db)

    async def get_by_email(self, email: str) -> UserEntity | None:
        """Get user by email address."""
        try:
            stmt = select(self.model).where(self.model.email == email)
            db_obj = await self.db.scalar(stmt)
            return self._to_entity(db_obj) if db_obj else None
        except SQLAlchemyError as e:
            raise ConflictException(
                f"Error retrieving user by email {email}: {str(e)}"
            ) from e

    async def get_by_username(self, username: str) -> UserEntity | None:
        """Get user by usernmae."""
        try:
            stmt = select(self.model).where(self.model.username == username)
            db_obj = await self.db.scalar(stmt)
            return self._to_entity(db_obj) if db_obj else None
        except SQLAlchemyError as e:
            raise ConflictException(
                f"Error retrieving user by email {username}: {str(e)}"
            ) from e

    async def exists_by_email(self, email: str) -> bool:
        """Check if a user with the given email exists."""
        try:
            stmt = select(exists().where(self.model.email == email))
            result = await self.db.scalar(stmt)
            return False if result is None else result
        except SQLAlchemyError as e:
            raise ConflictException(f"Error checking email existence: {str(e)}") from e

    async def update_last_login(self, user_id: UUID4) -> UserEntity:
        db_obj = await self._get_db_obj(user_id)
        if not db_obj:
            raise NotFoundException(f"User with id {user_id} not found")
        update_data = {"last_login": datetime.now(UTC).replace(tzinfo=None)}
        return await self.update(db_obj=db_obj, update_data=update_data)
