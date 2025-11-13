from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from src.core.error import AccessError, ConflictError, NotFoundError
from src.dependencies.users import get_current_user
from src.models.users import User
from src.schemas.tokens import TokenReadSchema
from src.schemas.users import (
    UserCreateSchema,
    UserLoginSchema,
    UserReadSchema,
    UserRegisterReadSchema,
)
from src.services.users import UserService, get_user_service

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
async def register(
    user_create: UserCreateSchema, user_service: Annotated[UserService, Depends(get_user_service)]
) -> User:
    try:
        user, token = await user_service.register(user_create)
        user.access_token = token
    except ConflictError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с такой электронной почтой уже зарегистрирован.",
        ) from None

    return user


@router.post(
    "/auth/login",
    tags=["Пользователи"],
    responses={
        200: {"description": "Успешный вход и возврат токена доступа."},
        404: {"description": "Пользователь с таким email не найден."},
        403: {"description": "Неверный пароль."},
    },
)
async def login(
    user_login: UserLoginSchema, user_service: Annotated[UserService, Depends(get_user_service)]
) -> TokenReadSchema:
    try:
        token = await user_service.login(user_login)
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь с таким email не найден."
        ) from None
    except AccessError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Неверный пароль.") from None

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
async def profile(user: Annotated[User, Depends(get_current_user)]) -> User:
    return user
