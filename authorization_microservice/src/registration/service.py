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

    async def generate_yandex_oauth_url(self) -> dict | HTTPException:
        """Создание url для авторизации через Yandex"""
        return await self._repository_generate_yandex_oauth_url()

    async def create_user_by_yandex(self, request: Request, oauth_token: str) -> dict | HTTPException:
        """Создание пользователя с помощью yandex oauth2"""
        return await self._repository_create_user_by_yandex(request, oauth_token)



async def init_registration_service(session: AsyncSession = Depends(get_session),
                                    user_session: AsyncSession = Depends(get_user_session)) -> RegistrationService:
    """Инициализация сервиса регистрации"""
    return RegistrationService(session, user_session)

