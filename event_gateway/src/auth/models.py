from sqlalchemy import Column, String, ARRAY, DateTime

from src.settings.models import AbstractModel


class UserModel(AbstractModel):
    """Модель пользователя"""
    __tablename__ = "users"

    username = Column(String(length=20), unique=False, nullable=False, comment="имя пользователя")
    email = Column(String(length=255), unique=False, nullable=False, comment="почта пользователя")
    avatar_url = Column(String(length=255), unique=False, nullable=True, comment="ссылка на аватарку пользователя")
    description = Column(String(length=190), unique=False, nullable=True, comment="описание пользователя")
    status = Column(String(length=30), unique=False, nullable=True, comment="статус пользователя")
    country = Column(String(255), unique=False, nullable=False, comment="страна пользователя")
    password = Column(String(255), unique=False, nullable=True, comment="пароль пользователя")
    clients_fingerprints = Column(ARRAY(String), unique=False, nullable=True,
                                  comment="ID устройств где была произведена авторизация")


class EmailAuthConfirmationCodeModel(AbstractModel):
    """Модель кода подтверждения авторизации"""
    __tablename__ = "auth_code"

    code = Column(String(), unique=False, nullable=False, comment="Код подтверждения")
    expire = Column(DateTime, nullable=False, comment="Срок действия")
