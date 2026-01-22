from pathlib import Path
from typing import Literal, final

from pydantic_settings import BaseSettings

BASE_PATH = Path(__file__).parent.parent.parent.parent.parent


def import_cert(path: Path) -> str:
    with open(path) as f:
        return f.read()


@final
class JWTSettings(BaseSettings):
    """JWT settings."""

    algorithm: Literal["RS256", "HS256"] = "RS256"
    access_token_expire_minutes: int = 60 * 24 * 8
    refresh_token_expire_minutes: int = 60 * 24 * 7
    private_key: str = import_cert(BASE_PATH / ".certs" / "jwt-private.pem")
    public_key: str = import_cert(BASE_PATH / ".certs" / "jwt-public.pem")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
