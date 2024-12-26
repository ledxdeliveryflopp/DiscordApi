from dataclasses import dataclass
from datetime import datetime
from http.client import HTTPException

import httpx
from sqlalchemy import Select
from starlette.requests import Request

from src.authorization.models import TokenModel, ConfirmationCodeModel
from src.authorization.schemas import LoginSchemas, YandexLoginSchemas, ConfirmLoginDeviceSchemas
from src.authorization.utils import verify_password, create_token, create_auth_token, get_token_payload, \
    create_confirmation_code
from src.broker.router import broker_service
from src.registration.models import UserModel
from src.settings.exceptions import UserDontExistException, BadPasswordException, YandexAuthException, \
    AddFingerprintException, EmptyXForwardedForHeader, ConfirmationCodeDontExistException, \
    ConfirmationCodeExpireException

from src.settings.service import BaseService


@dataclass
class AuthorizationRepository(BaseService):
    """Репозиторий авторизации"""

    async def _repository_find_user_by_email(self, email: str) -> UserModel:
        """Поиск пользователя по email"""
        user_in_db = await self.user_session.execute(Select(UserModel).where(UserModel.email == email))
        return user_in_db.scalar()

    async def _repository_find_user_by_id(self, user_id: int) -> UserModel:
        """Поиск пользователя по id"""
        user_in_db = await self.user_session.execute(Select(UserModel).where(UserModel.id == user_id))
        return user_in_db.scalar()

    async def _repository_find_confirmation_code(self, code: str) -> ConfirmationCodeModel:
        """Поиск кода подтверждения"""
        code_in_db = await self.email_session.execute(Select(ConfirmationCodeModel).where(ConfirmationCodeModel.code == code))
        return code_in_db.scalar()

    async def _repository_add_new_fingerprint_in_user(self, fingerprint: str, user_model: UserModel) -> None:
        """Добавить новое устройство авторизации пользователю"""
        try:
            new_list = []
            for i in user_model.clients_fingerprints:
                if i == fingerprint:
                    pass
                else:
                    new_list.append(i)
            new_list.append(fingerprint)
            user_model.clients_fingerprints = new_list
            await self.save_user_object(user_model)
        except Exception as exc:
            raise AddFingerprintException

    async def _repository_login(self, schemas: LoginSchemas, request: Request) -> dict:
        """Авторизация"""
        check_user = await self._repository_find_user_by_email(schemas.email)
        if not check_user:
            raise UserDontExistException
        check_password = await verify_password(schemas.password, check_user.password)
        if check_password is False:
            raise BadPasswordException
        if schemas.client_fingerprint not in check_user.clients_fingerprints:
            confirmation_code = await create_confirmation_code(check_user.id, schemas.client_fingerprint)
            user_ip = request.headers.get("X-Forwarded-For")
            if not user_ip:
                raise EmptyXForwardedForHeader
            await broker_service.send_email_data_in_queue(check_user.email, confirmation_code, user_ip)
            return {"detail": f"Confirmation code send to: {check_user.email}"}
        token_dict = await create_token(check_user.id, check_user.email)
        token = token_dict.get("token")
        expire = token_dict.get("expire")
        new_token_db = TokenModel(token=token, expire=expire)
        await self.save_object(new_token_db)
        return {"token": token, "type": "Bearer"}

    async def _repository_confirm_new_auth_device_and_login(self, schemas: ConfirmLoginDeviceSchemas):
        """Авторизация с кодом подтверждения"""
        check_user = await self._repository_find_user_by_email(schemas.email)
        if not check_user:
            raise UserDontExistException
        check_password = await verify_password(schemas.password, check_user.password)
        if check_password is False:
            raise BadPasswordException
        check_code = await self._repository_find_confirmation_code(schemas.confirmation_code)
        if not check_code:
            raise ConfirmationCodeDontExistException
        if check_code.expire < datetime.utcnow():
            await self.delete_email_object(check_code)
            raise ConfirmationCodeExpireException
        confirmation_code_data = await get_token_payload(schemas.confirmation_code)
        fingerprint = confirmation_code_data.get("client_fingerprint")
        await self._repository_add_new_fingerprint_in_user(fingerprint, check_user)
        token_dict = await create_token(check_user.id, check_user.email)
        token = token_dict.get("token")
        expire = token_dict.get("expire")
        new_token_db = TokenModel(token=token, expire=expire)
        await self.save_object(new_token_db)
        await self.delete_email_object(check_code)
        return {"token": token, "type": "Bearer"}

    async def _repository_login_by_yandex_with_token(self, oauth_token: str, schemas: YandexLoginSchemas) \
            -> dict | HTTPException:
        """Авторизация с помощью yandex по oauth токену"""
        request_header = {"Authorization": f"OAuth {oauth_token}"}
        response = httpx.get("https://login.yandex.ru/info?format=json", headers=request_header)
        if response.status_code != 200:
            raise YandexAuthException
        data = response.json()
        yandex_user_email = data.get("default_email")
        check_user = await self._repository_find_user_by_email(yandex_user_email)
        if not check_user:
            raise UserDontExistException
        token_dict = await create_token(check_user.id, check_user.email)
        token = token_dict.get("token")
        expire = token_dict.get("expire")
        new_token_db = TokenModel(token=token, expire=expire)
        await self.save_object(new_token_db)
        await self._repository_add_new_fingerprint_in_user(schemas.client_fingerprint, check_user)
        return {"token": token, "type": "Bearer"}

    async def _repository_create_encrypted_user_payload(self, request: Request) -> dict | HTTPException:
        """Создание токена с информацией о пользователе"""
        header_token = request.headers.get("Authorization")
        token_payload = await get_token_payload(header_token)
        user_id = token_payload.get("user_id")
        check_user = await self._repository_find_user_by_id(user_id)
        if not check_user:
            raise UserDontExistException
        user_email = token_payload.get("user_email")
        auth_token = await create_auth_token(user_id, user_email, check_user.password)
        return {"token": auth_token}

    async def _repository_login_by_auth_token(self, request: Request, client_id: str) -> dict | HTTPException:
        """Авторизация с помощью токена авторизации"""
        header_token = request.headers.get("Authorization")
        token_payload = await get_token_payload(header_token)
        user_id = token_payload.get("user_id")
        check_user = await self._repository_find_user_by_id(user_id)
        if not check_user:
            raise UserDontExistException
        user_hashed_password = token_payload.get("user_hashed_password")
        if check_user.password != user_hashed_password:
            raise BadPasswordException
        token_dict = await create_token(check_user.id, check_user.email)
        token = token_dict.get("token")
        expire = token_dict.get("expire")
        new_token_db = TokenModel(token=token, expire=expire)
        await self.save_object(new_token_db)
        await self._repository_add_new_fingerprint_in_user(client_id, check_user)
        return {"token": token, "type": "Bearer"}
