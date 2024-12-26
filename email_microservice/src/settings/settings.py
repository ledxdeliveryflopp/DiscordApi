from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


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


class KafkaSettings(BaseSettings):
    """Настройки для Kafka"""
    kafka_host: str
    kafka_port: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def get_full_kafka_path(self) -> str:
        """Создание полного url для бд"""
        return f"{self.kafka_host}:{self.kafka_port}"


class SMTPSettings(BaseSettings):
    """Настройки для smtp"""
    smtp_service: str
    smtp_port: str
    smtp_email_sender: str
    smtp_email_secret: str
    auth_return_url: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class Settings(BaseSettings):
    """Настройки"""
    database_settings: DatabaseSettings
    kafka_settings: KafkaSettings
    smtp_settings: SMTPSettings


@lru_cache()
def init_settings() -> Settings:
    """Инициализация настроек"""
    return Settings(database_settings=DatabaseSettings(), kafka_settings=KafkaSettings(), smtp_settings=SMTPSettings())


settings = init_settings()
