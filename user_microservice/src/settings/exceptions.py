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
