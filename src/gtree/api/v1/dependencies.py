from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from gtree.api.v1.schemas.user import UserSchema
from gtree.application.services.user_service import UserService
from gtree.infrastructure.db.repositories.user import UserRepository
from gtree.infrastructure.db.session import get_db

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))


async def get_current_active_user(
    token: str = Depends(oauth2_schema),
    user_service: UserService = Depends(get_user_service),
) -> UserSchema:
    return UserSchema.from_entity(
        await user_service.get_current_active_auth_user(token)
    )
