import smtplib
from dataclasses import dataclass
from datetime import datetime, timedelta

from faststream import Logger

from faststream.kafka import KafkaMessage

from src.auth.models import ConfirmationCodeModel
from src.auth.utils import fill_auth_template
from src.settings.broker import broker
from src.settings.service import base_service

from src.settings.settings import settings


@dataclass
class AuthEmailService:
    """Сервис отправки email сообщений для авторизации"""

    @broker.subscriber("auth-email-queue")
    async def send_auth_code(self, data: KafkaMessage, logger: Logger) -> None:
        logger.info(f"Message id: {data.message_id}")
        logger.info(f"Message info: {data.decoded_body}")
        user_email = data.decoded_body.get("user_email")
        confirmation_code = data.decoded_body.get("confirmation_code")
        user_ip = data.decoded_body.get("user_ip")
        sender = smtplib.SMTP(settings.smtp_settings.smtp_service, settings.smtp_settings.smtp_port)
        sender.ehlo()
        sender.starttls()
        sender.login(settings.smtp_settings.smtp_email_sender, settings.smtp_settings.smtp_email_secret)
        new_code = ConfirmationCodeModel(code=confirmation_code, expire=datetime.utcnow() + timedelta(minutes=10))
        await base_service.save_object(new_code)
        template = await fill_auth_template(user_email, confirmation_code, user_ip)
        sender.sendmail(settings.smtp_settings.smtp_service, user_email, template.as_string())
        sender.quit()
