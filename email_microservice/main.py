import asyncio

import aiokafka
from faststream import FastStream
from loguru import logger

from src.auth.service import AuthEmailService
from src.settings.broker import broker
from src.settings.config import alembic_ini_settings

app = FastStream(broker)


async def run_app() -> None:
    try:
        await app.run()
    except aiokafka.errors.KafkaConnectionError as exc:
        logger.debug(f"Start app exception: {exc}")


@app.on_startup
async def setup():
    AuthEmailService()

if __name__ == '__main__':
    logger.add("application.log", rotation="100 MB",
               format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}")
    alembic_ini_settings.set_database_url()
    asyncio.run(run_app())
