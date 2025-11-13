from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from src.core.error import AccessError, ConflictError, NotFoundError
from src.dependencies.users import get_current_user
from src.models.users import User
from src.schemas.tokens import TokenReadSchema, RefreshTokenSchema
from src.schemas.users import UserCreateSchema, UserLoginSchema, UserReadSchema, UserRegisterSchema
from src.services.users import UserService, get_user_service

router = APIRouter(prefix="/users")


@router.post(
    "/auth/register",
    tags=["Пользователи"],
    response_model=UserRegisterSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Успешная регистрация и возврат пользователя с токеном."},
        409: {"description": "Пользователь с такой электронной почтой уже зарегистрирован."},
    },
)
async def register(
    user_create: UserCreateSchema, user_service: Annotated[UserService, Depends(get_user_service)]
) -> UserRegisterSchema:
    try:
        schema = await user_service.register(user_create)
    except ConflictError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с такой электронной почтой уже зарегистрирован.",
        ) from None

    return schema


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
        return await user_service.login(user_login)
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь с таким email не найден."
        ) from None
    except AccessError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Неверный пароль.") from None


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


@router.post(
    "/token/refresh",
    tags=["Пользователи"],
    response_model=TokenReadSchema,
    responses={
        200: {"description": "Успешное обновление токенов, старый rerfesh больше не будет работать."},
        401: {"description": "Токен не действителен"},
    },
)
async def refresh_token(
    token_data: RefreshTokenSchema, user_service: Annotated[UserService, Depends(get_user_service)]
) -> TokenReadSchema:
    try:
        return await user_service.refresh_token(token_data.refresh_token)
    except AccessError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не действителен")
