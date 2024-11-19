import httpx
from passlib.context import CryptContext

from src.settings.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    """Хэширование пароля"""
    return pwd_context.hash(password)


async def get_user_country(ip: str) -> str:
    """Страна пользователя по ip"""
    async with httpx.AsyncClient() as client:
        request = await client.get(f"{settings.ipinfo_settings.ipinfo_url}{ip}"
                                   f"?token={settings.ipinfo_settings.ipinfo_token}")
        data = request.json()
        user_country = data.get("country")
    return user_country
