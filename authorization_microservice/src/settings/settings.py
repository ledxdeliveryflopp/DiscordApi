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


class EmailDatabaseSettings(BaseSettings):

    email_db_user: str
    email_db_password: str
    email_db_host: str
    email_db_port: str
    email_db_name: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def get_full_db_path(self) -> str:
        """Создание полного url для бд"""
        return (f"postgresql+asyncpg://{self.email_db_user}:{self.email_db_password}@"
                f"{self.email_db_host}:{self.email_db_port}/{self.email_db_name}")


class TokenSettings(BaseSettings):
    """Настройки токенов"""
    secret: str
    algorithm: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class IpInfoSettings(BaseSettings):
    """Настройки ipinfo"""
    ipinfo_url: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class YandexIdSettings(BaseSettings):
    """Настройки yandex id (для yandex oauth)"""
    client_id: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class KafkaSettings(BaseSettings):
    """Настройки для Kafka"""
    kafka_host: str
    kafka_port: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def get_full_kafka_path(self) -> str:
        """Создание полного url для бд"""
        return f"{self.kafka_host}:{self.kafka_port}"


class Settings(BaseSettings):
    """Настройки"""
    api_settings: ApiSettings
    database_settings: DatabaseSettings
    user_database_settings: UserDatabaseSettings
    email_database_settings: EmailDatabaseSettings
    token_settings: TokenSettings
    ipinfo_settings: IpInfoSettings
    yandex_id_settings: YandexIdSettings
    kafka_settings: KafkaSettings


@lru_cache()
def init_settings() -> Settings:
    """Инициализация настроек"""
    return Settings(api_settings=ApiSettings(), database_settings=DatabaseSettings(),
                    user_database_settings=UserDatabaseSettings(), email_database_settings=EmailDatabaseSettings(),
                    token_settings=TokenSettings(), ipinfo_settings=IpInfoSettings(),
                    yandex_id_settings=YandexIdSettings(), kafka_settings=KafkaSettings())


settings = init_settings()

