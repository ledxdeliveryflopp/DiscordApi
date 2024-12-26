from faststream.kafka.fastapi import KafkaRouter

from src.settings.settings import settings


kafka_router = KafkaRouter(settings.kafka_settings.get_full_kafka_path, schema_url="/asyncapi",
                           include_in_schema=True)


class BrokerService:

    @staticmethod
    async def send_email_data_in_queue(user_email: str, confirmation_code: str, user_ip: str) -> None:
        await kafka_router.broker.publish({"user_email": user_email, "confirmation_code": confirmation_code,
                                           "user_ip": user_ip}, "auth-email-queue")


broker_service = BrokerService()
