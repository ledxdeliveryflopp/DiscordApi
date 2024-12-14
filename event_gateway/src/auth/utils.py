import random
import string
from datetime import datetime, timedelta
from http import client

import httpx
from jose import jwt
from loguru import logger

from src.settings.settings import settings


async def check_token_payload(token: str) -> bool:
    """Проверка токена"""
    decoded_token = jwt.decode(token, settings.token_settings.secret, algorithms=settings.token_settings.algorithm)
    user_id = decoded_token.get("user_id", None)
    user_email = decoded_token.get("user_email", None)
    user_hashed_password = decoded_token.get("user_hashed_password", None)
    if not user_email or not user_hashed_password or not user_id:
        return False
    return True


async def get_user_id_from_token(user_data: str) -> int | None:
    decoded_token = jwt.decode(user_data, settings.token_settings.secret, algorithms=settings.token_settings.algorithm)
    user_id = decoded_token.get("user_id", None)
    return user_id


async def create_confirmation_code(user_id: int) -> str:
    """Создание токена подтверждения"""
    random_string = random.choices(string.printable, k=10)
    token_payload = {"user_id": user_id, "random": random_string}
    token = jwt.encode(token_payload, settings.token_settings.secret, algorithm=settings.token_settings.algorithm)
    return token


async def get_request_user_ip() -> str | None:
    """IP пользователя"""
    user_ip_request = httpx.get("https://ipinfo.io/ip")
    user_ip = user_ip_request.text
    logger.debug(f"user ip: {user_ip}")
    if not user_ip or user_ip_request.status_code != 200:
        return None
    return user_ip
