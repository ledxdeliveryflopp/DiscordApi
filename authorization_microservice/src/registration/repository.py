from dataclasses import dataclass
from fastapi import HTTPException
from sqlalchemy import Select, Result, CursorResult
from starlette.requests import Request

from src.registration.models import UserModel
from src.registration.schemas import CreateUserSchemas
from src.registration.utils import get_user_country, hash_password
from src.settings.exceptions import UserExistException
from src.settings.service import BaseService


@dataclass
class RegistrationRepository(BaseService):
    """Репозиторий регистрации"""

    async def _repository_find_user_by_email(self, email: str) -> Result | CursorResult:
        """Поиск пользователя по email"""
        user = await self.user_session.execute(Select(UserModel).where(UserModel.email == email))
        return user.scalar()

    async def _repository_create_user(self, schemas: CreateUserSchemas, request: Request) -> dict | HTTPException:
        """Создание пользователя"""
        user = await self._repository_find_user_by_email(schemas.email)
        if user:
            raise UserExistException
        user_country = await get_user_country(request)
        new_user = UserModel(**schemas.dict(exclude={"password", "country"}), password=hash_password(schemas.password),
                             country=user_country)
        await self.save_user_object(new_user)
        return {"detail": "success"}
