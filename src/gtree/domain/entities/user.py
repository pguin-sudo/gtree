from dataclasses import dataclass, field
from datetime import datetime
import re
from typing import Literal

from gtree.domain.entities.base import BaseEntity, ObjectBaseEntity
from gtree.domain.exceptions import DomainValidationException
from gtree.domain.funcs.time import get_current_time


@dataclass(kw_only=True, slots=True)
class UserEntity(ObjectBaseEntity):
    """User entity representing a system user."""

    username: str
    email: str
    password_hash: bytes = field(default=b"")
    is_verified: bool = field(default=False)
    last_login: datetime = field(default_factory=get_current_time)
    last_password_change: datetime = field(default_factory=get_current_time)

    def __post_init__(self):
        if not (2 <= len(self.username) <= 64):
            raise DomainValidationException(
                "Username must be between 2 and 64 characters long"
            )
        if not re.match(r"^[a-zA-Z0-9_.-]+$", self.username):
            raise DomainValidationException(
                "Username must contain only alphanumeric characters, underscores, dots, or hyphens"
            )

        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise DomainValidationException("Invalid email address format")

        if not isinstance(self.password_hash, bytes):
            raise DomainValidationException("password_hash must be of type bytes")

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
        try:
            return cls(
                username=username,
                email=email,
                password_hash=password_hash,
                is_verified=is_verified,
                last_login=last_login or get_current_time(),
                last_password_change=last_password_change or get_current_time(),
            )
        except DomainValidationException:
            raise

    def update_last_login(self):
        self.last_login = get_current_time()
        self.__post_init__()

    def __repr__(self) -> str:
        return f"<UserEntity(id='{self.id}', email='{self.email}'>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UserEntity):
            return False
        return self.id == other.id


@dataclass(kw_only=True, slots=True)
class TokenEntity(BaseEntity):
    """Token entity representing a user token."""

    access_token: str
    refresh_token: str
    token_type: Literal["Bearer"] = "Bearer"
