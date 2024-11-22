from dataclasses import dataclass

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.authorization.repository import AuthorizationRepository
from src.authorization.schemas import LoginSchemas
from src.settings.database import get_session


@dataclass
class AuthorizationService(AuthorizationRepository):
    """Сервис авторизации"""

    async def login(self, schemas: LoginSchemas) -> dict:
        """Авторизация"""
        return await self._repository_login(schemas)


async def init_authorization_service(session: AsyncSession = Depends(get_session)) -> AuthorizationService:
    """Инициализация сервиса авторизации"""
    return AuthorizationService(session)

