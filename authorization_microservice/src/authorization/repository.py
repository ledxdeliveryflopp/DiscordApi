from dataclasses import dataclass
from http.client import HTTPException

import httpx
from sqlalchemy import Select

from src.authorization.models import TokenModel
from src.authorization.schemas import LoginSchemas
from src.authorization.utils import verify_password, create_token
from src.registration.models import UserModel
from src.settings.exceptions import UserDontExistException, BadPasswordException, YandexAuthException
from src.settings.service import BaseService


@dataclass
class AuthorizationRepository(BaseService):
    """Репозиторий авторизации"""

    async def _find_user_by_email(self, email: str) -> UserModel:
        """Поиск пользователя по email"""
        user = await self.user_session.execute(Select(UserModel).where(UserModel.email == email))
        return user.scalar()

    async def _repository_login(self, schemas: LoginSchemas) -> dict:
        """Авторизация"""
        check_user = await self._find_user_by_email(schemas.email)
        if not check_user:
            raise UserDontExistException
        check_password = await verify_password(schemas.password, check_user.password)
        if check_password is False:
            raise BadPasswordException
        token_dict = await create_token(check_user.id, check_user.email)
        token = token_dict.get("token")
        expire = token_dict.get("expire")
        new_token_db = TokenModel(token=token, expire=expire)
        await self.save_object(new_token_db)
        return {"token": token, "type": "Bearer"}

    async def _repository_login_by_yandex_with_token(self, oauth_token: str) -> dict | HTTPException:
        """Авторизация с помощью yandex по oauth токену"""
        request_header = {"Authorization": f"OAuth {oauth_token}"}
        response = httpx.get("https://login.yandex.ru/info?format=json", headers=request_header)
        if response.status_code != 200:
            raise YandexAuthException
        data = response.json()
        yandex_user_email = data.get("default_email")
        check_user = await self._find_user_by_email(yandex_user_email)
        if not check_user:
            raise UserDontExistException
        token_dict = await create_token(check_user.id, check_user.email)
        token = token_dict.get("token")
        expire = token_dict.get("expire")
        new_token_db = TokenModel(token=token, expire=expire)
        await self.save_object(new_token_db)
        return {"token": token, "type": "Bearer"}
