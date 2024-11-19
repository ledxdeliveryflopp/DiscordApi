from typing import Any

from fastapi import HTTPException
from starlette import status


class DetailedHTTPException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Server error"

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail, **kwargs)


class SaveException(DetailedHTTPException):
    status_code = 400
    detail = "save error."


class UserExistException(DetailedHTTPException):
    status_code = 400
    detail = "User already exist."


class UserDontExistException(DetailedHTTPException):
    status_code = 404
    detail = "User dont exist."
