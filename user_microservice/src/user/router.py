from fastapi import APIRouter, Depends
from starlette.requests import Request

from src.user.schemas import CreateUserSchemas, UserFindResponseSchemas
from src.user.service import UserService, init_user_service

user_router = APIRouter(prefix="/users", tags=["user"])


@user_router.get("/user/", response_model=list[UserFindResponseSchemas])
async def router_find_user_by_username(username: str, service: UserService = Depends(init_user_service)):
    """Поиск пользователя по username"""
    return await service.find_user_by_username(username)


@user_router.post("/register/")
async def router_create_user(schemas: CreateUserSchemas, request: Request,
                             service: UserService = Depends(init_user_service)):
    """Создание пользоваталя"""
    return await service.create_user(schemas, request)
