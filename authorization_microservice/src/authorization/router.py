from fastapi import APIRouter, Depends
from starlette.requests import Request

from src.authorization.schemas import LoginSchemas, YandexLoginSchemas, ConfirmLoginDeviceSchemas
from src.authorization.service import AuthorizationService, init_authorization_service

auth_router = APIRouter(prefix="/auth", tags=['authorization'])


@auth_router.post("/login/")
async def router_login(schemas: LoginSchemas, request: Request,
                       service: AuthorizationService = Depends(init_authorization_service)):
    """Роутер авторизации"""
    return await service.login(schemas, request)


@auth_router.post("/confirm_device_and_login/")
async def router_confirm_new_auth_device_and_login(schemas: ConfirmLoginDeviceSchemas,
                                                   service: AuthorizationService = Depends(init_authorization_service)):
    """Роутер авторизации с кодом подтверждения"""
    return await service.confirm_new_auth_device_and_login(schemas)


@auth_router.post("/login_yandex/")
async def router_login_by_yandex(oauth_token: str, schemas: YandexLoginSchemas,
                                 service: AuthorizationService = Depends(init_authorization_service)):
    """Роутер авторизации через Yandex ID"""
    return await service.login_by_yandex(oauth_token, schemas)


@auth_router.get("/encrypt_user_data/")
async def router_create_encrypted_user_payload(request: Request,
                                               service: AuthorizationService = Depends(init_authorization_service)):
    """Получение qr кода для авторизации"""
    return await service.create_encrypted_user_payload(request)


@auth_router.get("/qr_auth/")
async def router_login_by_qr_code(client_id: str, request: Request,
                                  service: AuthorizationService = Depends(init_authorization_service)):
    """Роутер авторизации по qr коду"""
    return await service.login_by_auth_token(request, client_id)

