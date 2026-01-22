from typing import Literal, final
from uuid import UUID

from gtree.api.v1.schemas.base import BaseSchema


@final
class TokenSchema(BaseSchema):
    """Schema for JWT token data"""

    access_token: str
    refresh_token: str
    token_type: Literal["Bearer"] = "Bearer"


@final
class UserSchema(BaseSchema):
    """Schema with basic user data"""

    id: UUID
    email: str
    username: str
    is_active: bool
