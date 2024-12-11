from fastapi import APIRouter, Depends
from starlette.requests import Request

from src.registration.schemas import CreateUserSchemas
from src.registration.service import RegistrationService, init_registration_service
from src.registration.utils import get_user_country

registration_router = APIRouter(prefix="/auth", tags=["register"])


@registration_router.post("/register/")
async def router_create_user(schemas: CreateUserSchemas, request: Request,
                             service: RegistrationService = Depends(init_registration_service)):
    """Создание пользоваталя"""
    return await service.create_user(schemas, request)


@registration_router.get('/current_ip/')
async def get_ip(request: Request):
    country = await get_user_country(request)
    return {"detail": country}


@registration_router.get("/yandex_oauth_url/")
async def router_generate_yandex_oauth_url(service: RegistrationService = Depends(init_registration_service)):
    """Создание url для авторизации через Yandex"""
    return await service.generate_yandex_oauth_url()


@registration_router.post("/yandex_oauth_register/")
async def router_create_user_by_yandex(oauth_token: str, request: Request,
                                       service: RegistrationService = Depends(init_registration_service)):
    """Создание пользователя с помощью yandex oauth2"""
    return await service.create_user_by_yandex(request, oauth_token)
