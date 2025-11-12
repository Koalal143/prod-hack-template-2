from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi_cache.decorator import cache

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


@router.post("/auth/register", tags=["Пользователи"], response_model=UserRegisterReadSchema)
async def register(
    user_create: UserCreateSchema, user_service: Annotated[UserService, Depends(get_user_service)]
) -> User:
    try:
        user, token = await user_service.register(user_create)
        user.access_token = token
    except ConflictError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с такой электронной почтой уже зарегистрирован.",
        ) from None

    return user


@router.post("/auth/login", tags=["Пользователи"])
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


@router.get("/profile", tags=["Пользователи"], response_model=UserReadSchema)
@cache(expire=60)  # просто пример (конкретно тут это НЕ будет работать из-за зависимости)
async def profile(user: Annotated[User, Depends(get_current_user)]) -> User:
    return user
