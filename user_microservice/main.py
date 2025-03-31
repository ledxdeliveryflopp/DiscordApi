from fastapi import FastAPI
import uvicorn
from prometheus_client import Summary, start_http_server, make_asgi_app
from starlette.middleware.cors import CORSMiddleware

from src.settings.config import alembic_ini_settings
from src.settings.settings import settings
from src.user.router import user_router

user_app = FastAPI()

metrics_app = make_asgi_app()

user_app.include_router(user_router)
user_app.mount("/metrics", metrics_app)

origins = ["*"]


user_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
)


def run_app(host: str, port: int) -> None:
    """Запуск приложения"""
    uvicorn.run(app=user_app, host=host, port=port, log_config="log.ini")


if __name__ == '__main__':
    alembic_ini_settings.set_database_url()
    run_app(settings.api_settings.api_host, settings.api_settings.api_port)
