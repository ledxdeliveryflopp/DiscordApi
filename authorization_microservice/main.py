import aiokafka
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from src.authorization.router import auth_router
from src.broker.router import kafka_router
from src.registration.router import registration_router
from src.settings.config import alembic_ini_settings
from src.settings.settings import settings

authorization_app = FastAPI()


authorization_app.include_router(registration_router)
authorization_app.include_router(auth_router)
authorization_app.include_router(kafka_router)

origins = ["*"]

authorization_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def run_app(host: str, port: int) -> None:
    """Запуск приложения"""
    uvicorn.run(app=authorization_app, host=host, port=port, log_config="log.ini")


if __name__ == '__main__':
    alembic_ini_settings.set_database_url()
    logger.add("application.log", rotation="100 MB",
               format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}")
    run_app(settings.api_settings.api_host, settings.api_settings.api_port)
