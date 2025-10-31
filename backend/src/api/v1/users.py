from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from src.core.auth.dependencies import get_current_user
from src.core.error import NotFoundError, AccessError
from src.models.users import User
from src.schemas.tokens import TokenReadSchema
from src.services.users import UserService, get_user_service
from src.schemas.users import (
    UserCreateSchema,
    UserRegisterReadSchema,
    UserLoginSchema,
    UserReadSchema,
)

user_rt = APIRouter(prefix="/users")


@user_rt.post(
    "/auth/register", tags=["Пользователи"], response_model=UserRegisterReadSchema
)
async def register(
    user_create: UserCreateSchema, user_service: UserService = Depends(get_user_service)
):
    try:
        user, token = await user_service.register(user_create)
        user.access_token = token
    except UserWithEmailAlreadyExistsError:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с такой электронной почтой уже зарегистрирован.",
        )

    return user


@user_rt.post("/auth/login", tags=["Пользователи"], response_model=TokenReadSchema)
async def login(
    user_login: UserLoginSchema, user_service: UserService = Depends(get_user_service)
):
    try:
        token = await user_service.login(user_login)
    except NotFoundError:
        raise HTTPException(
            status_code=404, detail="Пользователь с таким email не найден."
        )
    except AccessError:
        raise HTTPException(status_code=403, detail="Неверный пароль.")

    return TokenReadSchema(access_token=token)


#
# @user_rt.post("/auth/refresh", tags=["Пользователи"])
# async def refresh_token():
#     pass
#
@user_rt.get("/profile", tags=["Пользователи"], response_model=UserReadSchema)
async def profile(user: User = Depends(get_current_user)):
    return user
