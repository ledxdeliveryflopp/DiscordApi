import smtplib
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiofiles
from jinja2 import Template

from src.settings.settings import settings


@dataclass
class EmailService:
    """Сервис отправки mail уведомлений"""

    @staticmethod
    async def __fill_template(user_email: str, login_ip: str, confirmation_code: str) -> MIMEMultipart:
        """Заполнение html"""
        async with aiofiles.open("src/email/static/templates/new_auth_device.html", "r") as file:
            template_data = await file.read()
        jinja_template = Template(template_data)
        data = {"subject": "Login attempt from an unknown device", "greeting": f"Dear {user_email}",
                "message": f"A new login location has been detected from ip: {login_ip}, please confirm your login.",
                "confirmation_code": f"Confirmation code: {confirmation_code}",
                "expire": "The code is valid for 10 minutes"}
        message_content = jinja_template.render(data)
        message = MIMEMultipart()
        message["subject"] = "Login attempt from an unknown device"
        message.attach(MIMEText(message_content, "html"))
        return message

    async def send_email_message(self, user_email: str, login_ip: str, confirmation_code: str) -> None:
        """Отправка email уведомления"""
        sender = smtplib.SMTP(settings.smtp_settings.smtp_service, settings.smtp_settings.smtp_port)
        sender.ehlo()
        sender.starttls()
        sender.login(settings.smtp_settings.smtp_email_sender, settings.smtp_settings.smtp_email_secret)
        template = await self.__fill_template(user_email, login_ip, confirmation_code)
        sender.sendmail(settings.smtp_settings.smtp_service, user_email, template.as_string())
        sender.quit()


email_service = EmailService()
