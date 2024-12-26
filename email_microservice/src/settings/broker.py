from faststream.kafka import KafkaBroker

from src.settings.settings import settings

broker = KafkaBroker(settings.kafka_settings.get_full_kafka_path)
