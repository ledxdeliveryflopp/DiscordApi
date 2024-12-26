import httpx
from passlib.context import CryptContext
from starlette.requests import Request

from src.settings.exceptions import EmptyXForwardedForHeader, EmptyAcceptLanguage
from src.settings.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    """Хэширование пароля"""
    return pwd_context.hash(password)


async def get_user_country(request: Request) -> str:
    """Страна пользователя по ip или accept-language"""
    forwarder_for = request.headers.get("X-Forwarded-For")
    if not forwarder_for:
        raise EmptyXForwardedForHeader
    async with httpx.AsyncClient() as client:
        ip_info = await client.get(f"{settings.ipinfo_settings.ipinfo_url}{forwarder_for}/json")
        if ip_info.status_code != 200:
            accept_lang = request.headers.get("accept-language")
            if not accept_lang:
                raise EmptyAcceptLanguage
            country_code = accept_lang.split(",")[0]
            return country_code
        ip_info_json = ip_info.json()
        ip_info_country = ip_info_json.get("country")
        return ip_info_country
