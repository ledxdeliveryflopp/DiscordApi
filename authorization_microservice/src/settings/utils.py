from src.settings.settings import settings


async def generate_yandex_oauth_url() -> dict:
    """Создание url для авторизации через Yandex"""
    oauth_yandex_url = (f"https://oauth.yandex.ru/authorize?"
                        f"response_type=token&client_id={settings.yandex_id_settings.client_id}")
    return {"yandex_url": oauth_yandex_url}
