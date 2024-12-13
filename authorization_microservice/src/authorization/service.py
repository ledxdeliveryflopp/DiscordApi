from dataclasses import dataclass
from http.client import HTTPException

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from src.authorization.repository import AuthorizationRepository
from src.authorization.schemas import LoginSchemas
from src.settings.database import get_session, get_user_session


@dataclass
class AuthorizationService(AuthorizationRepository):
    """Сервис авторизации"""

    async def login(self, schemas: LoginSchemas) -> dict:
        """Авторизация"""
        return await self._repository_login(schemas)

    async def login_by_yandex(self, oauth_token: str) -> dict | HTTPException:
        """Авторизация через Yandex ID"""
        return await self._repository_login_by_yandex_with_token(oauth_token)

    async def create_encrypted_user_payload(self, request: Request) -> dict | HTTPException:
        """Создание токена авторизации для авторизации через qr код"""
        return await self._repository_create_encrypted_user_payload(request)

    async def login_by_auth_token(self, request: Request, client_id) -> dict | HTTPException:
        """Авторизация с помощью токена авторизации"""
        return await self._repository_login_by_auth_token(request, client_id)


async def init_authorization_service(session: AsyncSession = Depends(get_session),
                                     user_session: AsyncSession = Depends(get_user_session)) -> AuthorizationService:
    """Инициализация сервиса авторизации"""
    return AuthorizationService(session, user_session)

