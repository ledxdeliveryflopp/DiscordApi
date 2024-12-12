from fastapi import FastAPI
import uvicorn
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware

from src.settings.config import alembic_ini_settings
from src.settings.settings import settings
from src.user.router import user_router

user_app = FastAPI()

user_app.include_router(user_router)

origins = ["*"]

user_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
)

def custom_openapi():
    if user_app.openapi_schema:
        return user_app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        summary="This is a very custom OpenAPI schema",
        description="Here's a longer description of the custom **OpenAPI** schema",
        routes=user_app.routes,
    )
    openapi_schema["components"]["schemas"].update({"test": [1, 2]})
    user_app.openapi_schema = openapi_schema
    return user_app.openapi_schema


user_app.openapi = custom_openapi


def run_app(host: str, port: int) -> None:
    """Запуск приложения"""
    uvicorn.run(app=user_app, host=host, port=port, log_config="log.ini")


if __name__ == '__main__':
    alembic_ini_settings.set_database_url()
    run_app(settings.api_settings.api_host, settings.api_settings.api_port)
