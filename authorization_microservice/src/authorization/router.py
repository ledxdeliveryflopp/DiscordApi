from fastapi import APIRouter, Depends

from src.authorization.schemas import LoginSchemas
from src.authorization.service import AuthorizationService, init_authorization_service

auth_router = APIRouter(prefix="/auth", tags=['authorization'])


@auth_router.post("/login/")
async def router_login(schemas: LoginSchemas, service: AuthorizationService = Depends(init_authorization_service)):
    """Роутер авторизации"""
    return await service.login(schemas)
