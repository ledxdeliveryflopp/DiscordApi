from pydantic import BaseModel, Field, EmailStr


class BaseUserSchemas(BaseModel):
    """Базовая схема пользователя"""
    id: int


class CreateUserSchemas(BaseModel):
    """Схема создания пользователя"""
    username: str = Field(min_length=4, max_length=20)
    email: EmailStr
    description: str = Field(max_length=190)
    status: str = Field(max_length=30)
    password: str = Field(min_length=5, max_length=255)


class UserFindResponseSchemas(BaseUserSchemas):
    """Схема пользователя при поиске"""
    username: str
    avatar_url: str | None
