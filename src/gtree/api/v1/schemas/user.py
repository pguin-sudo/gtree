from typing import Literal, final
from uuid import UUID

from gtree.api.v1.schemas.base import BaseSchema
from gtree.domain.entities.user import TokenEntity, UserEntity


@final
class TokenResponseSchema(BaseSchema):
    """Schema for JWT token data"""

    access_token: str
    refresh_token: str
    token_type: Literal["Bearer"] = "Bearer"

    @classmethod
    def from_entity(cls, entity: TokenEntity) -> "TokenResponseSchema":
        return TokenResponseSchema(
            access_token=entity.access_token,
            refresh_token=entity.refresh_token,
            token_type=entity.token_type,
        )


@final
class UserResponseSchema(BaseSchema):
    """Schema with basic user data"""

    id: UUID
    email: str
    username: str
    is_active: bool

    @classmethod
    def from_entity(cls, entity: UserEntity) -> "UserResponseSchema":
        return UserResponseSchema(
            id=entity.id,
            email=entity.email,
            username=entity.username,
            is_active=entity.is_active,
        )
