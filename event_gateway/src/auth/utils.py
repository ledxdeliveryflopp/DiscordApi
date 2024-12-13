from jose import jwt

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


async def get_user_data(user_data: str) -> bool:
    decoded_token = jwt.decode(user_data, settings.token_settings.secret, algorithms=settings.token_settings.algorithm)
    user_id = decoded_token.get("user_id", None)
    user_email = decoded_token.get("user_email", None)
    user_hashed_password = decoded_token.get("user_hashed_password", None)
    if not user_id or not user_email or not user_hashed_password:
        return False
    return True
