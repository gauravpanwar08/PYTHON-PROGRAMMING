# ==================================================================================
#              PYDANTIC SETTINGS - CONFIGURATION
#
# BaseSettings       → Loads configuration from environment variables and .env files.
# SettingsConfigDict → Configures how settings are loaded.
# SecretStr          → Keeps sensitive values protected
# .env               → Stores actual configuration separately from Python code
# ===================================================================================


from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


# Application Settings

class Settings(BaseSettings):

    # Application

    app_name: str
    app_version: str
    debug: bool

    # Database

    database_url: str

    # Redis

    redis_url: str

    # Security

    secret_key: SecretStr

    # Server

    host: str
    port: int

    # Settings Configuration

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


# Create Settings Object

settings = Settings()
