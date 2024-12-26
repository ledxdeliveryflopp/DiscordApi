from pydantic import BaseModel, EmailStr


class BaseLoginSchemas(BaseModel):
    client_fingerprint: str


class LoginSchemas(BaseLoginSchemas):
    """Схема логина"""
    email: EmailStr
    password: str


class YandexLoginSchemas(BaseLoginSchemas):
    """Схема логина через Yandex"""
    pass


class ConfirmLoginDeviceSchemas(BaseModel):
    """Схема логина с кодом подтверждения"""
    email: EmailStr
    password: str
    confirmation_code: str
