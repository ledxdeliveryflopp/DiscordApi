from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from src.auth.router import auth_events_router
from src.settings.settings import settings

avents_gateway = FastAPI()

avents_gateway.include_router(auth_events_router)

origins = ["*"]

avents_gateway.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
)

def run_app(host: str, port: int) -> None:
    """Запуск приложения"""
    uvicorn.run(app=avents_gateway, host=host, port=port, log_config="log.ini")


if __name__ == '__main__':
    run_app(settings.api_settings.api_host, settings.api_settings.api_port)
