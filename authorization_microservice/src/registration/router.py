from fastapi import APIRouter, Depends
from starlette.requests import Request

from src.registration.schemas import CreateUserSchemas
from src.registration.service import RegistrationService, init_registration_service
from src.registration.utils import get_user_country

registration_router = APIRouter(prefix="/authorization", tags=["register"])


@registration_router.post("/register/")
async def router_create_user(schemas: CreateUserSchemas, request: Request,
                             service: RegistrationService = Depends(init_registration_service)):
    """Создание пользоваталя"""
    return await service.create_user(schemas, request)


@registration_router.get('/current_ip/')
async def get_ip(request: Request):
    country = await get_user_country(request)
    return {"detail": country}
