from pydantic import Field
from pydantic_settings import BaseSettings

from gtree.core.config.app import AppSettings
from gtree.core.config.cors import CORSSettings
from gtree.core.config.database import DatabaseSettings
from gtree.core.config.jwt import JWTSettings


class Settings(BaseSettings):
    """Main application settings that combines all configuration objects.

    This class serves as a facade that provides access to all configuration
    sections of the application. Each configuration section is responsible
    for a specific domain (database, redis, cors, etc.).
    """

    app: AppSettings = Field(default_factory=AppSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    cors: CORSSettings = Field(default_factory=CORSSettings)
    jwt: JWTSettings = Field(default_factory=JWTSettings)


settings = Settings()
