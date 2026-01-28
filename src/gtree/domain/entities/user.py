from datetime import datetime
from typing import Literal

from pydantic import EmailStr, Field

from gtree.domain.entities.base import BaseEntity, ObjectBaseEntity
from gtree.domain.funcs.time import get_current_time


class UserEntity(ObjectBaseEntity):
    """User entity representing a system user."""

    username: str = Field(
        min_length=2,
        max_length=64,
        pattern=r"^[a-zA-Z0-9_.-]+$",
        description="Unique username",
    )
    email: EmailStr = Field(description="User email address")
    password_hash: bytes = Field(default=b"", description="Hashed password")
    is_verified: bool = Field(default=False, description="Email verification status")
    last_login: datetime = Field(
        default_factory=get_current_time, description="Last login timestamp"
    )
    last_password_change: datetime = Field(
        default_factory=get_current_time,
        description="Last password change timestamp",
    )

    @classmethod
    def create_user(
        cls,
        username: str,
        email: str,
        password_hash: bytes = b"",
        *,
        is_verified: bool = False,
        last_login: datetime | None = None,
        last_password_change: datetime | None = None,
    ) -> "UserEntity":
        """Create a new user entity."""
        return UserEntity(
            username=username,
            email=email,
            password_hash=password_hash,
            is_verified=is_verified,
            last_login=last_login or get_current_time(),
            last_password_change=last_password_change or get_current_time(),
        )

    def update_last_login(self):
        self.last_login = get_current_time()

    def __repr__(self) -> str:
        return f"<UserEntity(id='{self.id}', email='{self.email}')>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UserEntity):
            return False
        return self.id == other.id


class TokenEntity(BaseEntity):
    """Token entity representing a user token."""

    access_token: str
    refresh_token: str
    token_type: Literal["Bearer"] = "Bearer"
