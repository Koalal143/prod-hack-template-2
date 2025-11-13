from datetime import timedelta
from typing import Annotated

from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from src.core.error import AccessError, ConflictError, NotFoundError
from src.core.security import create_token, get_password_hash, verify_password
from src.models.users import User
from src.repositories.users import UserRepository, get_user_repository
from src.schemas.users import UserCreateSchema, UserLoginSchema
from src.services.base import BaseService


class UserService(BaseService[UserRepository]):
    async def register(self, user_create: UserCreateSchema) -> tuple[User, str]:
        """
        Регистрирует нового пользователя и возвращает его вместе с access токеном
        """
        user_create_dict = user_create.model_dump()
        user_create_dict.pop("password")
        user_create_dict["password_hash"] = get_password_hash(user_create.password)

        try:
            user = await self.repository.create(user_create_dict)
        except IntegrityError:
            raise ConflictError from None

        token = create_token(data={"sub": str(user.email)}, expires_delta=timedelta(hours=7))
        return user, token

    async def login(self, user_login: UserLoginSchema) -> str:
        """
        Получение токена по паролю и почте
        """
        user = await self.repository.get_by_email(user_login.email)
        if user is None:
            raise NotFoundError

        if not verify_password(user_login.password, user.password_hash):
            raise AccessError

        return create_token(data={"sub": user.email}, expires_delta=timedelta(hours=7))


async def get_user_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    return UserService(user_repository)
