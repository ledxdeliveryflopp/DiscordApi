from sqlalchemy import Column, Integer, DateTime, func

from src.settings.database import Base


class AbstractModel(Base):
    """Абстрактная модель"""
    __abstract__ = True

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, comment="id объекта")
    created_at = Column(DateTime, server_default=func.now(), comment="Дата создания")
