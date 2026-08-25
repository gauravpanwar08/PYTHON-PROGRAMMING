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


# --------------------------------------------------------
# Settings Model
# --------------------------------------------------------

class Settings(BaseSettings):

    # Application settings

    app_name: str
    app_version: str
    debug: bool

    # Server settings

    host: str
    port: int

    # Database settings

    database_url: str

    # Redis settings

    redis_url: str

    # Secret

    secret_key: SecretStr

    # Settings configuration

    model_config = SettingsConfigDict(
        env_file=".env",           # have to create .env file to load here otherwise this will raise an error
        env_file_encoding="utf-8",
        extra="ignore"
    )


# --------------------------------------------------------
# Create Settings Object
# --------------------------------------------------------

settings = Settings()


# --------------------------------------------------------
# Print Settings
# --------------------------------------------------------

print("Application Name:")
print(settings.app_name)

print("\nApplication Version:")
print(settings.app_version)

print("\nDebug:")
print(settings.debug)

print("\nDebug Type:")
print(type(settings.debug))

print("\nHost:")
print(settings.host)

print("\nPort:")
print(settings.port)

print("\nPort Type:")
print(type(settings.port))

print("\nDatabase URL:")
print(settings.database_url)

print("\nRedis URL:")
print(settings.redis_url)


# --------------------------------------------------------
# SecretStr
# --------------------------------------------------------

print("\nSecret Key:")
print(settings.secret_key)

print("\nActual Secret Value:")
print(settings.secret_key.get_secret_value())
