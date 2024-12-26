from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiofiles
import httpx
from jinja2 import Template

from src.settings.settings import settings


async def get_lat_lon_by_ip(ip_address: str) -> dict | None:
    """Получение широты/долготы по ip"""
    request_body = {"ip": [{"address": ip_address}]}
    request = httpx.post("https://locator.api.maps.yandex.ru/v1/locate?apikey=b9da27e2-8440-4561-8a09-c0c9781410a1",
                         json=request_body)
    if request.status_code == 200:
        response_json = request.json()
        lat = response_json["location"]["point"]["lat"]
        lon = response_json["location"]["point"]["lon"]
        return {"lat": lat, "lon": lon}


async def get_location_by_ip_address(ip_address: str) -> str:
    """Создание карты"""
    location = await get_lat_lon_by_ip(ip_address)
    lat = location.get("lat")
    lon = location.get("lon")
    map_url = (f"https://static-maps.yandex.ru/v1?ll={lon},{lat}&size=500,300&spn=0.016457,0.00619"
               f"&lang=en_US&theme=dark&pt={lon},{lat},round&apikey=ad4bb57c-60d0-44e2-9c4b-de499e9879d8")
    return map_url


async def fill_auth_template(user_email: str, confirmation_code: str, user_ip: str) -> MIMEMultipart:
    """Заполнение html"""
    async with aiofiles.open("src/auth/static/templates/new_auth_device.html", "r") as file:
        template_data = await file.read()
    jinja_template = Template(template_data)
    map_location = await get_location_by_ip_address(user_ip)
    auth_href = f"{settings.smtp_settings.auth_return_url}{confirmation_code}"
    data = {"user_email": user_email, "auth_href": auth_href, "ip": user_ip}
    message_content = jinja_template.render(data, yandex_static_map=map_location)
    message = MIMEMultipart()
    message["subject"] = "Login attempt from an unknown device"
    message.attach(MIMEText(message_content, "html"))
    return message
