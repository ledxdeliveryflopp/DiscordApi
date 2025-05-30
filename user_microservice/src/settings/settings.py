from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseSettings):
    """Настройки api"""
    api_host: str
    api_port: int

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class DatabaseSettings(BaseSettings):
    """Настройки БД"""
    user: str
    password: str
    host: str
    port: str
    name: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def get_full_db_path(self) -> str:
        """Создание полного url для бд"""
        return (f"postgresql+asyncpg://{self.user}:{self.password}@"
                f"{self.host}:{self.port}/{self.name}")


class S3Settings(BaseSettings):
    """Настройки S3"""
    secret_access_key: str
    secret_key_id: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class TokenSettings(BaseSettings):
    """Настройки токенов"""
    jwt_secret: str
    algorithm: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class Settings(BaseSettings):
    """Настройки"""
    api_settings: ApiSettings
    database_settings: DatabaseSettings
    s3_settings: S3Settings
    token_settings: TokenSettings


@lru_cache()
def init_settings() -> Settings:
    """Инициализация настроек"""
    return Settings(api_settings=ApiSettings(), database_settings=DatabaseSettings(), s3_settings=S3Settings(),
                    token_settings=TokenSettings())


settings = init_settings()

