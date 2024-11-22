from fastapi import FastAPI
import uvicorn

from src.authorization.router import auth_router
from src.registration.router import registration_router
from src.settings.config import alembic_ini_settings
from src.settings.settings import settings

authorization_app = FastAPI()

authorization_app.include_router(registration_router)
authorization_app.include_router(auth_router)


def run_app(host: str, port: int) -> None:
    """Запуск приложения"""
    uvicorn.run(app=authorization_app, host=host, port=port, log_config="log.ini")


if __name__ == '__main__':
    alembic_ini_settings.set_database_url()
    run_app(settings.api_settings.api_host, settings.api_settings.api_port)
