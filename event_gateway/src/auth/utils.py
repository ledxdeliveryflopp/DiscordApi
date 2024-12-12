from jose import jwt

from src.settings.settings import settings


async def get_user_id_from_token(token: str) -> str:
    """Получение id пользователя из токена"""
    decoded_token = jwt.decode(token, settings.token_settings.secret, algorithms=settings.token_settings.algorithm)
    user_id = decoded_token.get("user_id")
    return user_id

