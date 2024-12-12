import random
import string
from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from src.settings.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def create_token(user_id: int, user_email: str) -> dict:
    """Создание токена"""
    random_string = random.choices(string.printable, k=10)
    expire_date = datetime.utcnow() + timedelta(minutes=30)
    token_payload = {"user_id": user_id, "user_email": user_email, "random": random_string}
    token = jwt.encode(token_payload, settings.token_settings.secret, algorithm=settings.token_settings.algorithm)
    return {"token": token, "expire": expire_date}


async def get_token_payload(token: str) -> dict:
    """Получение нагрузки токена"""
    decoded_token = jwt.decode(token, settings.token_settings.secret, algorithms=settings.token_settings.algorithm)
    return decoded_token


async def create_auth_token(user_email: str) -> str:
    """Генерация токена для авторизации по QR"""
    random_string = random.choices(string.printable, k=5)
    token_payload = {"user_email": user_email, "random": random_string}
    auth_token = jwt.encode(token_payload, settings.token_settings.secret, algorithm=settings.token_settings.algorithm)
    return auth_token
