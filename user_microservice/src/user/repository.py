from dataclasses import dataclass
from typing import Any, Sequence

from fastapi import HTTPException
from sqlalchemy import Select, Result, CursorResult, Row, RowMapping
from starlette.requests import Request

from src.settings.exceptions import UserExistException
from src.settings.service import BaseService
from src.user.models import UserModel
from src.user.schemas import CreateUserSchemas
from src.user.utils import hash_password


@dataclass
class UserRepository(BaseService):
    """Репозиторий пользователей"""

    async def _repository_find_user_by_email(self, email: str) -> Result | CursorResult:
        """Поиск пользователя по email"""
        user = await self.session.execute(Select(UserModel).where(UserModel.email == email))
        return user.scalar()

    async def _repository_find_user_by_username(self, username: str) -> Sequence[Row[Any] | RowMapping | Any]:
        """Поиск пользователя по username"""
        user = await self.session.execute(Select(UserModel).where(UserModel.username == username))
        return user.scalars().all()

    async def _repository_create_user(self, schemas: CreateUserSchemas, request: Request) -> dict | HTTPException:
        """Создание пользователя"""
        user = await self._repository_find_user_by_email(schemas.email)
        if user:
            raise UserExistException
        client_host = request.headers.get("accept-language")
        country = client_host.split(",")[0]
        new_user = UserModel(**schemas.dict(exclude={"password", "country"}), password=hash_password(schemas.password),
                             country=country)
        await self.save_object(new_user)
        return {"detail": "success"}
