from typing import Any

from fastapi import HTTPException
from starlette import status


class DetailedHTTPException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Server error"

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail, **kwargs)


class SaveException(DetailedHTTPException):
    """Ошибка сохранения в БД"""
    status_code = 400
    detail = "save error."


class UserExistException(DetailedHTTPException):
    """Пользователь уже существует"""
    status_code = 400
    detail = "User already exist."


class UserDontExistException(DetailedHTTPException):
    """Пользователя не существует"""
    status_code = 404
    detail = "User dont exist."


class UserIpException(DetailedHTTPException):
    """Не удалось определить страну пользователя"""
    status_code = 400
    detail = "It is not possible to determine the country, turn off the VPN or try later."


class BadPasswordException(DetailedHTTPException):
    """Не верный пароль"""
    status_code = 403
    detail = "Bad password."


class YandexAuthException(DetailedHTTPException):
    """Не удалось авторизировать через Yandex"""
    status_code = 400
    detail = "Bad status code from Yandex."


class EmptyXForwardedForHeader(DetailedHTTPException):
    """Пустой заголовок X-Forwarded-For"""
    status_code = 400
    detail = "Empty X-Forwarded-For header."


class EmptyAcceptLanguage(DetailedHTTPException):
    """Пустой заголовок accept-language"""
    status_code = 400
    detail = "Empty accept-language header."


class AddFingerprintException(DetailedHTTPException):
    """ошибка при добавлении устройства"""
    status_code = 400
    detail = "Error while add new auth device."


class ConfirmationCodeDontExistException(DetailedHTTPException):
    """Кода потдверждения уже существует"""
    status_code = 404
    detail = "Confirmation code dont exist."


class ConfirmationCodeExpireException(DetailedHTTPException):
    """Срок действия кода подтверждения истек"""
    status_code = 400
    detail = "Confirmation code expired."

