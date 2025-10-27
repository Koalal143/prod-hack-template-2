from fastapi import APIRouter
from fastapi.params import Depends

from dependencies.users import get_user_service
from services.users import UserService
from schemas.users import UserCreateSchema

user_rt = APIRouter(prefix="/users")


# @user_rt.get("/profile", tags=["Пользователи"])
# async def profile():
#     pass
#
#
@user_rt.post("/auth/register", tags=["Пользователи"])
async def register(user_create: UserCreateSchema, user_service: UserService = Depends(get_user_service)):
    pass


#
#
# @user_rt.post("/auth/login", tags=["Пользователи"])
# async def login():
#     pass
#
#
# @user_rt.post("/auth/refresh", tags=["Пользователи"])
# async def refresh_token():
#     pass
