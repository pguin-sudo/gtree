from datetime import UTC, datetime
from typing import Literal

from pydantic import EmailStr, Field

from gtree.domain.entities.base import BaseEntity, ObjectBaseEntity


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
        default_factory=lambda: datetime.now(UTC), description="Last login timestamp"
    )
    last_password_change: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Last password change timestamp",
    )

    def __repr__(self) -> str:
        return f"<User(id='{self.id}', email='{self.email}')>"

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UserEntity):
            return False
        return self.id == other.id


class TokenEntity(BaseEntity):
    """Token entity representing a user token."""

    access_token: str
    refresh_token: str
    token_type: Literal["Bearer"] = "Bearer"
