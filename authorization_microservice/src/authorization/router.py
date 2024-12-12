from fastapi import APIRouter, Depends

from src.authorization.schemas import LoginSchemas
from src.authorization.service import AuthorizationService, init_authorization_service

auth_router = APIRouter(prefix="/auth", tags=['authorization'])


@auth_router.post("/login/")
async def router_login(schemas: LoginSchemas, service: AuthorizationService = Depends(init_authorization_service)):
    """Роутер авторизации"""
    return await service.login(schemas)


@auth_router.post("/login_yandex/")
async def router_login_by_yandex(oauth_token: str, service: AuthorizationService = Depends(init_authorization_service)):
    """Роутер авторизации через Yandex ID"""
    return await service.login_by_yandex(oauth_token)


@auth_router.get("/get_qr_url/")
async def router_create_auth_qr_code(service: AuthorizationService = Depends(init_authorization_service)):
    """Получение qr кода для авторизации"""
    return await service.get_qr_code_url()


@auth_router.get("/qr_auth/")
async def router_login_by_qr_code(auth_token: str, service: AuthorizationService = Depends(init_authorization_service)):
    """Роутер авторизации по qr коду"""
    return await service.login_by_qr_code(auth_token)

