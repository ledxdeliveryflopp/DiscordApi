from fastapi import FastAPI
import uvicorn

from src.settings.config import alembic_ini_settings
from src.settings.settings import settings
from src.user.router import user_router

user_app = FastAPI()

user_app.include_router(user_router)


def run_app(host: str, port: int) -> None:
    """Запуск приложения"""
    uvicorn.run(app=user_app, host=host, port=port, log_config="log.ini")


if __name__ == '__main__':
    alembic_ini_settings.set_database_url()
    run_app(settings.api_settings.api_host, settings.api_settings.api_port)
