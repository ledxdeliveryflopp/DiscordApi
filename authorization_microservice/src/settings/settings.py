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


class UserDatabaseSettings(BaseSettings):

    user_db_user: str
    user_db_password: str
    user_db_host: str
    user_db_port: str
    user_db_name: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def get_full_db_path(self) -> str:
        """Создание полного url для бд"""
        return (f"postgresql+asyncpg://{self.user_db_user}:{self.user_db_password}@"
                f"{self.user_db_host}:{self.user_db_port}/{self.user_db_name}")


class TokenSettings(BaseSettings):
    """Настройки токенов"""
    secret: str
    algorithm: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class IpInfoSettings(BaseSettings):
    """Настройки ipinfo"""
    ipinfo_url: str
    ipinfo_token: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class Settings(BaseSettings):
    """Настройки"""
    api_settings: ApiSettings
    database_settings: DatabaseSettings
    user_database_settings: UserDatabaseSettings
    token_settings: TokenSettings
    ipinfo_settings: IpInfoSettings


@lru_cache()
def init_settings() -> Settings:
    """Инициализация настроек"""
    return Settings(api_settings=ApiSettings(), database_settings=DatabaseSettings(),
                    user_database_settings=UserDatabaseSettings(), token_settings=TokenSettings(),
                    ipinfo_settings=IpInfoSettings())


settings = init_settings()

