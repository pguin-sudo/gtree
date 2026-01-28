from datetime import timedelta
from uuid import UUID

from gtree.application.exceptions import (
    InvalidCredentialsException,
    InvalidTokenException,
    UserInactiveException,
)
from gtree.domain.entities.user import TokenEntity, UserEntity
from gtree.infrastructure.db.repositories.user import UserRepository
from gtree.infrastructure.utils import auth as auth_utils


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def validate_auth_user(self, username: str, password: str) -> UserEntity:
        user = await self.user_repository.get_by_username(username)
        if not user:
            raise InvalidCredentialsException("Invalid email or password")
        if not auth_utils.verify_password(password, user.password_hash):
            raise InvalidCredentialsException("Invalid email or password")
        if not user.is_active:
            raise UserInactiveException("User account is inactive")
        return user

    async def register(self, username: str, password: str, email: str) -> TokenEntity:
        hashed_password = auth_utils.hash_password(password)
        created_user = UserEntity.create_user(
            username=username, email=email, password_hash=hashed_password
        )
        user = await self.user_repository.create(created_user)
        jwt_payload = {
            "sub": str(user.id),
            "email": user.email,
            "username": user.username,
        }
        access_token = auth_utils.encode_jwt(jwt_payload)
        refresh_token = auth_utils.encode_jwt(
            jwt_payload, expire_timedelta=timedelta(days=30)
        )
        return TokenEntity(access_token=access_token, refresh_token=refresh_token)

    async def login(self, username: str, password: str) -> TokenEntity:
        user: UserEntity = await self.validate_auth_user(username, password)
        user.update_last_login()
        _ = await self.user_repository.update(user)
        jwt_payload = {
            "sub": str(user.id),
            "email": user.email,
            "username": user.username,
        }
        access_token = auth_utils.encode_jwt(jwt_payload)
        refresh_token = auth_utils.encode_jwt(
            jwt_payload, expire_timedelta=timedelta(days=30)
        )
        return TokenEntity(access_token=access_token, refresh_token=refresh_token)

    async def get_current_auth_user(self, token: str) -> UserEntity:
        try:
            payload = auth_utils.decode_jwt(token=token)
            sub: str | None = payload.get("sub")
            if sub is not None:
                user_id = UUID(sub)
                if user := await self.user_repository.get_by_id(user_id):
                    return user
        except (ValueError, auth_utils.InvalidTokenError):
            pass

        raise InvalidTokenException("Token invalid")

    async def get_current_active_auth_user(self, token: str) -> UserEntity:
        user = await self.get_current_auth_user(token)
        if not user.is_active:
            raise UserInactiveException("User account is inactive")
        return user
