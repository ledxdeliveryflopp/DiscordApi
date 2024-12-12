from pydantic import BaseModel, EmailStr


class LoginSchemas(BaseModel):
    """Схема логина"""
    email: EmailStr
    password: str
