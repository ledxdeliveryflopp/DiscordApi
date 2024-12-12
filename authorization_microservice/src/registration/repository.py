from dataclasses import dataclass

import httpx
from fastapi import HTTPException
from sqlalchemy import Select, Result, CursorResult
from starlette.requests import Request

from src.authorization.utils import create_auth_token
from src.registration.models import UserModel
from src.registration.schemas import CreateUserSchemas
from src.registration.utils import get_user_country, hash_password
from src.settings.exceptions import UserExistException
from src.settings.service import BaseService
from src.settings.utils import generate_yandex_oauth_url


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
        auth_token = await create_auth_token(schemas.email)
        new_user = UserModel(**schemas.dict(exclude={"password", "country"}), password=hash_password(schemas.password),
                             country=user_country, qr_auth_token=auth_token)
        await self.save_user_object(new_user)
        return {"detail": "success"}

    @staticmethod
    async def _repository_generate_yandex_oauth_url() -> dict | HTTPException:
        """Создание url для авторизации через Yandex"""
        oauth_yandex_url = await generate_yandex_oauth_url()
        return oauth_yandex_url

    async def _repository_create_user_by_yandex(self, request: Request, oauth_token: str) -> dict | HTTPException:
        """Создание пользователя с помощью yandex oauth2"""
        try:
            request_header = {"Authorization": f"OAuth {oauth_token}"}
            response = httpx.get("https://login.yandex.ru/info?format=json", headers=request_header).json()
            yandex_user_login = response.get("login")
            yandex_user_email = response.get("default_email")
            yandex_user_avatar_id = response.get("default_avatar_id")
            yandex_user_avatar_url = (f"https://avatars.yandex.net/get-yapic/"
                                      f"{yandex_user_avatar_id}/islands-retina-50")
            user_country = await get_user_country(request)
            new_user = UserModel(username=yandex_user_login, email=yandex_user_email,
                                 avatar_url=yandex_user_avatar_url, country=user_country)
            await self.save_user_object(new_user)
            return {"detail": "success"}
        except Exception as exception:
            raise HTTPException(detail=exception, status_code=400)
