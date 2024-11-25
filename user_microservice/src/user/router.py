from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.security import HTTPBearer
from starlette.requests import Request

from src.user.schemas import UserFindResponseSchemas
from src.user.service import UserService, init_user_service

user_router = APIRouter(prefix="/users", tags=["user"])


@user_router.get("/user/", response_model=list[UserFindResponseSchemas])
async def router_find_user_by_username(username: str, service: UserService = Depends(init_user_service)):
    """Поиск пользователя по username"""
    return await service.find_user_by_username(username)


@user_router.patch("/upload-avatar/", response_model=None)
async def router_upload_avatar(request: Request, avatar_file: UploadFile = File(),
                               service: UserService = Depends(init_user_service)):
    return await service.upload_avatar(request, avatar_file)
