from dataclasses import dataclass

from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from src.user_microservice.settings.database import get_session
from src.user_microservice.user.repository import UserRepository
from src.user_microservice.user.schemas import CreateUserSchemas


@dataclass
class UserService(UserRepository):
    """Сервис пользователей"""

    async def create_user(self, schemas: CreateUserSchemas, request: Request) -> dict | HTTPException:
        """Создание пользователя"""
        return await self._repository_create_user(schemas, request)


async def init_user_service(session: AsyncSession = Depends(get_session)):
    """Инициализация сервиса пользователей"""
    return UserService(session)

