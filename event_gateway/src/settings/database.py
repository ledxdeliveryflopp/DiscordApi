from typing import Generator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from src.settings.settings import settings

engine = create_async_engine(url=settings.database_settings.get_full_db_path, echo=False)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

email_engine = create_async_engine(url=settings.email_database_settings.get_full_db_path, echo=False)

email_async_session = sessionmaker(email_engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_session() -> Generator:
    """Сессия бд"""
    async with async_session() as session:
        yield session


async def get_email_session() -> Generator:
    """Сессия бд email сообщений"""
    async with email_async_session() as session:
        yield session
