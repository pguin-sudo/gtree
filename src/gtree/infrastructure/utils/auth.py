from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
import jwt

from gtree.core.config.settings import settings
from gtree.infrastructure.utils.exceptions import InvalidTokenError


def hash_password(password: str) -> bytes:
    """Hash password using bcrypt and return bytes for storage."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


def verify_password(password: str, hashed_password: bytes) -> bool:
    """Verify password against stored hash (bytes)."""
    return bcrypt.checkpw(password.encode(), hashed_password)


def encode_jwt(
    payload: dict[str, Any],
    private_key: str | None = None,
    algorithm: str = settings.jwt.algorithm,
    expire_timedelta: timedelta | None = None,
    expire_minutes: int = settings.jwt.access_token_expire_minutes,
) -> str:
    """Encode JWT token with optional expiration."""
    if private_key is None:
        private_key = settings.jwt.private_key
    to_encode = payload.copy()
    now = datetime.now(UTC)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire, iat=now)
    encoded: str = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str | None = None,
    algorithm: str = settings.jwt.algorithm,
) -> dict[str, Any]:
    """Decode and validate JWT token."""
    if public_key is None:
        public_key = settings.jwt.public_key
    try:
        decoded: dict[str, Any] = jwt.decode(token, public_key, algorithms=[algorithm])
        return decoded
    except jwt.InvalidTokenError as e:
        raise InvalidTokenError(str(e)) from e
