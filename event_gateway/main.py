from fastapi import FastAPI
import uvicorn
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from src.auth.router import auth_events_router
from src.broker.router import kafka_router
from src.settings.settings import settings

events_gateway = FastAPI()

events_gateway.include_router(auth_events_router)
events_gateway.include_router(kafka_router)


origins = ["*"]

events_gateway.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
)


def run_app(host: str, port: int) -> None:
    """Запуск приложения"""
    uvicorn.run(app=events_gateway, host=host, port=port, log_config="log.ini")


if __name__ == '__main__':
    logger.add("application.log", rotation="100 MB",
               format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}")
    run_app(settings.api_settings.api_host, settings.api_settings.api_port)
