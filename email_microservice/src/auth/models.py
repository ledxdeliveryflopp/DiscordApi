from sqlalchemy import Column, String, DateTime

from src.settings.models import AbstractModel


class ConfirmationCodeModel(AbstractModel):
    """Модель кодов подтверждения авторизации"""
    __tablename__ = "confirmation_code"

    code = Column(String, nullable=False, comment="код подтверждения")
    expire = Column(DateTime, nullable=False, comment="Срок действия")
