from dataclasses import dataclass

from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from src.registration.repository import RegistrationRepository
from src.registration.schemas import CreateUserSchemas
from src.settings.database import get_session, get_user_session


@dataclass
class RegistrationService(RegistrationRepository):
    """Сервис регистрации"""

    async def create_user(self, schemas: CreateUserSchemas, request: Request) -> dict | HTTPException:
        """Создание пользователя"""
        return await self._repository_create_user(schemas, request)


async def init_registration_service(session: AsyncSession = Depends(get_session),
                                    user_session: AsyncSession = Depends(get_user_session)) -> RegistrationService:
    """Инициализация сервиса регистрации"""
    return RegistrationService(session, user_session)

