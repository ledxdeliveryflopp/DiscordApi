from pydantic import BaseModel


class BaseUserSchemas(BaseModel):
    """Базовая схема пользователя"""
    id: int


class UserFindResponseSchemas(BaseUserSchemas):
    """Схема пользователя при поиске"""
    username: str
    avatar_url: str | None
