from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi_cache.decorator import cache

from src.dependencies.users import get_current_user
from src.core.error import NotFoundError, AccessError, ConflictError
from src.models.users import User
from src.schemas.tokens import TokenReadSchema
from src.services.users import UserService, get_user_service
from src.schemas.users import (
    UserCreateSchema,
    UserRegisterReadSchema,
    UserLoginSchema,
    UserReadSchema,
)


router = APIRouter(prefix="/users")


@router.post(
    "/auth/register",
    tags=["Пользователи"],
    response_model=UserRegisterReadSchema,
    responses={
        200: {"description": "Успешная регистрация и возврат пользователя с токеном."},
        409: {"description": "Пользователь с такой электронной почтой уже зарегистрирован."},
    },
)
async def register(user_create: UserCreateSchema, user_service: UserService = Depends(get_user_service)):
    try:
        user, token = await user_service.register(user_create)
        user.access_token = token
    except ConflictError:
        raise HTTPException(
            status_code=409,
            detail="Пользователь с такой электронной почтой уже зарегистрирован.",
        )

    return user


@router.post(
    "/auth/login",
    tags=["Пользователи"],
    response_model=TokenReadSchema,
    responses={
        200: {"description": "Успешный вход и возврат токена доступа."},
        404: {"description": "Пользователь с таким email не найден."},
        403: {"description": "Неверный пароль."},
    },
)
async def login(user_login: UserLoginSchema, user_service: UserService = Depends(get_user_service)):
    try:
        token = await user_service.login(user_login)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Пользователь с таким email не найден.")
    except AccessError:
        raise HTTPException(status_code=403, detail="Неверный пароль.")

    return TokenReadSchema(access_token=token)


@router.get(
    "/profile",
    tags=["Пользователи"],
    response_model=UserReadSchema,
    responses={
        200: {"description": "Успешный возврат данных текущего пользователя."},
        401: {"description": "Пользователь не авторизован (не предоставлен или недействителен токен)."},
    },
)
async def profile(user: User = Depends(get_current_user)):
    return user
