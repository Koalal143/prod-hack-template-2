from datetime import timedelta
from typing import Tuple

from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from src.core.error import ConflictError, NotFoundError, AccessError
from src.services.base import BaseService
from src.core.security import get_password_hash, create_token, verify_password
from src.models.users import User
from src.repositories.users import UserRepository, get_user_repository
from src.schemas.users import UserCreateSchema, UserLoginSchema


class UserService(BaseService[UserRepository]):
    async def register(self, user_create: UserCreateSchema) -> Tuple[User, str]:
        """
        Регистрирует нового пользователя и возвращает его вместе с access токеном
        """

        user_create_dict = user_create.model_dump()
        user_create_dict.pop("password")
        user_create_dict["password_hash"] = get_password_hash(user_create.password)

        try:
            user = await self.repository.create(user_create_dict)
        except IntegrityError:
            raise ConflictError

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

        token = create_token(data={"sub": user.email}, expires_delta=timedelta(hours=7))
        return token


async def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repository)
