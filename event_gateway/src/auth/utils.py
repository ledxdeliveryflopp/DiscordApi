import random
import string

from jose import jwt, JWTError
from loguru import logger

from src.settings.settings import settings


async def check_token_payload(token: str) -> bool:
    """Проверка токена"""
    try:
        decoded_token = jwt.decode(token, settings.token_settings.secret, algorithms=settings.token_settings.algorithm)
        user_id = decoded_token.get("user_id", None)
        user_email = decoded_token.get("user_email", None)
        user_hashed_password = decoded_token.get("user_hashed_password", None)
        if not user_email or not user_hashed_password or not user_id:
            return False
        return True
    except JWTError as jwt_exc:
        logger.debug(f"jwt error: {jwt_exc}")
        return False


async def get_user_id_from_token(user_data: str) -> int | None:
    decoded_token = jwt.decode(user_data, settings.token_settings.secret, algorithms=settings.token_settings.algorithm)
    user_id = decoded_token.get("user_id", None)
    return user_id


async def create_confirmation_code(user_id: int, client_fingerprint: str) -> str:
    """Создание токена подтверждения"""
    token_payload = {"user_id": user_id, "client_fingerprint": client_fingerprint}
    token = jwt.encode(token_payload, settings.token_settings.secret, algorithm=settings.token_settings.algorithm)
    return token
