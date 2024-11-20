import httpx
from passlib.context import CryptContext
from starlette.requests import Request

from src.settings.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    """Хэширование пароля"""
    return pwd_context.hash(password)


async def get_user_country(request: Request) -> str:
    """Страна пользователя по ip"""
    try:
        async with httpx.AsyncClient() as client:
            user_ip_request = httpx.get("https://ipinfo.io/ip")
            user_ip = user_ip_request.text
            request = await client.get(f"{settings.ipinfo_settings.ipinfo_url}{user_ip}"
                                       f"?token={settings.ipinfo_settings.ipinfo_token}")
            data = request.json()
            user_country = data.get("country")
        return user_country
    except Exception as exception:
        client_host = request.headers.get("accept-language")
        country = client_host.split(",")[0]
        return country
