from pydantic import BaseModel, Field, EmailStr


class CreateUserSchemas(BaseModel):
    """Схема создания пользователя"""
    username: str = Field(min_length=4, max_length=20)
    email: EmailStr
    description: str = Field(max_length=190)
    status: str = Field(max_length=30)
    password: str = Field(min_length=5, max_length=255)

