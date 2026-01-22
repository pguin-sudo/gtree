from datetime import datetime
from typing import override

from pydantic import dataclasses
from sqlalchemy import Boolean, DateTime, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.expression import text

from gtree.domain.entities.user import UserEntity
from gtree.infrastructure.db.models.base import ObjectBaseModel


class UserModel(ObjectBaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    password_hash: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    last_login: Mapped[datetime] = mapped_column(
        DateTime, server_default=text("TIMEZONE('utc', now())"), nullable=False
    )
    last_password_change: Mapped[datetime] = mapped_column(
        DateTime, server_default=text("TIMEZONE('utc', now())"), nullable=False
    )

    @override
    def __repr__(self) -> str:
        return f"<User(id='{self.id}', email='{self.email}')>"

    @classmethod
    @override
    def from_entity(cls, entity: UserEntity) -> "UserModel":
        data = dataclasses.asdict(entity)
        return cls(
            id=data["id"],
            username=data["username"],
            email=data["email"],
            password_hash=data["password_hash"],
            is_verified=data["is_verified"],
            last_login=data["last_login"],
            last_password_change=data["last_password_change"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            is_active=data["is_active"],
        )
