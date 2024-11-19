from dataclasses import dataclass
from typing import Any, Sequence

from fastapi import HTTPException, Depends
from sqlalchemy import Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from src.settings.database import get_session
from src.settings.exceptions import UserDontExistException
from src.user.repository import UserRepository
from src.user.schemas import CreateUserSchemas


@dataclass
class UserService(UserRepository):
    """Сервис пользователей"""

    async def find_user_by_username(self, username: str) -> Sequence[Row[Any] | RowMapping | Any]:
        """Поиск пользователя по username"""
        user = await self._repository_find_user_by_username(username)
        if not user:
            raise UserDontExistException
        return user

    async def create_user(self, schemas: CreateUserSchemas, request: Request) -> dict | HTTPException:
        """Создание пользователя"""
        return await self._repository_create_user(schemas, request)


async def init_user_service(session: AsyncSession = Depends(get_session)):
    """Инициализация сервиса пользователей"""
    return UserService(session)

