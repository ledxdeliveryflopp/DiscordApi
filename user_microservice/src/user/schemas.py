from pydantic import BaseModel


class BaseUserSchemas(BaseModel):
    """Базовая схема пользователя"""
    id: int


class UserFindResponseSchemas(BaseUserSchemas):
    """Схема пользователя при поиске"""
    username: str
    avatar_url: str | None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "10",
                    "username": "LedxDelivery",
                    "avatar_url": "https://tinyurl.com/26jwb9r4",
                }
            ]
        }
    }
