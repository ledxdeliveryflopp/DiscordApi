from jose import jwt

from src.settings.settings import settings


async def decode_token(token: str) -> dict:
    token_data = jwt.decode(token, settings.token_settings.jwt_secret, algorithms=['HS256'])
    return token_data
