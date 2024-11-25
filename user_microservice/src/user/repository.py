from dataclasses import dataclass
from typing import Any, Sequence

import aiofiles
from fastapi import File
from sqlalchemy import Select, Row, RowMapping
from starlette.requests import Request

from src.settings.service import BaseService
from src.user.models import UserModel
from src.user.s3 import s3_service
from src.user.utils import decode_token


@dataclass
class UserRepository(BaseService):
    """Репозиторий пользователей"""

    async def _repository_find_user_by_email(self, email: str) -> UserModel:
        """Поиск пользователя по email"""
        user = await self.session.execute(Select(UserModel).where(UserModel.email == email))
        return user.scalar()

    async def _repository_find_user_by_id(self, user_id: str) -> UserModel:
        """Поиск пользователя по email"""
        user = await self.session.execute(Select(UserModel).where(UserModel.id == user_id))
        return user.scalar()

    async def _repository_get_user_by_token(self, request: Request) -> UserModel:
        request_header = request.headers.get("Authorization")
        token_data = await decode_token(request_header)
        user_id = token_data.get("user_id")
        user = await self._repository_find_user_by_id(user_id)
        return user

    async def _repository_find_user_by_username(self, username: str) -> Sequence[Row[Any] | RowMapping | Any]:
        """Поиск пользователя по username"""
        user = await self.session.execute(Select(UserModel).where(UserModel.username == username))
        return user.scalars().all()

    async def _repository_upload_avatar(self, request: Request, avatar_file: File()) -> dict:
        user = await self._repository_get_user_by_token(request)
        filename = avatar_file.filename
        async with aiofiles.open(f"temp/{filename}", "wb") as file:
            file_data = await avatar_file.read()
            await file.write(file_data)
        avatar_url = await s3_service.upload_file_in_s3(filename)
        user.avatar_url = avatar_url
        await self.save_object(user)
        return {"Detail": "success"}
