from datetime import timedelta
from typing import Tuple

from sqlalchemy.exc import IntegrityError

from core.service import BaseService
from core.auth.security import get_password_hash, create_token, verify_password
from errors.users import (
    UserWithEmailAlreadyExistsError,
    UserNotFoundError,
    UserPasswordIsIncorrectError,
)
from models.users import User
from repositories.users import UserRepository
from schemas.users import UserCreateSchema, UserLoginSchema


class UserService(BaseService[UserRepository]):
    async def register(self, user_create: UserCreateSchema) -> Tuple[User, str]:
        """
        регистрирует нового пользователя и возвращает его вместе с access токеном
        :return:
        """

        user_create_dict = user_create.model_dump()
        user_create_dict.pop("password")
        user_create_dict["password_hash"] = get_password_hash(user_create.password)

        try:
            user = await self.repository.create(user_create_dict)
        except IntegrityError:
            raise UserWithEmailAlreadyExistsError

        token = create_token(
            data={"sub": str(user.email)}, expires_delta=timedelta(hours=7)
        )
        return user, token

    async def login(self, user_login: UserLoginSchema) -> str:
        user = await self.repository.get_by_email(user_login.email)
        if user is None:
            raise UserNotFoundError

        if not verify_password(user_login.password, user.password_hash):
            raise UserPasswordIsIncorrectError

        token = create_token(data={"sub": user.email}, expires_delta=timedelta(hours=7))
        return token

    async def logout(self):
        pass

    async def refresh_token(self):
        pass
