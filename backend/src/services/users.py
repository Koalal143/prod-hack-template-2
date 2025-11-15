import uuid
from datetime import timedelta
from typing import Annotated

from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from src.core.error import AccessError, ConflictError, NotFoundError
from src.core.security import create_token, get_string_hash, verify_hash, verify_token
from src.models.users import User
from src.repositories.tokens import TokenRepository, get_token_repository
from src.repositories.users import UserRepository, get_user_repository
from src.schemas.tokens import TokenReadSchema
from src.schemas.users import UserCreateSchema, UserLoginSchema, UserReadSchema, UserRegisterSchema
from src.settings import settings


class UserService:
    def __init__(self, user_repository: UserRepository, token_repository: TokenRepository) -> None:
        """
        Зависит сразу от двух репозиториев, поэтому не наследуется от базового класса
        """
        self.user_repository = user_repository
        self.token_repository = token_repository

    @staticmethod
    async def _create_access_token(user: User) -> str:
        """
        Генерация access токена
        """
        return create_token(
            data={"sub": user.email},
            expires_delta=timedelta(seconds=settings.ACCESS_TOKEN_LIFETIME),
            token_type="access",
        )

    async def _create_refresh_token(self, user: User) -> str:
        """
        Генерация refresh токена, также заносится в бд, чтобы после использования его удалить
        """
        token_id = str(uuid.uuid4())

        token = create_token(
            data={"sub": user.email, "id": token_id},
            expires_delta=timedelta(seconds=settings.REFRESH_TOKEN_LIFETIME),
            token_type="refresh",
        )
        await self.token_repository.create({"token_hash": get_string_hash(token), "id": token_id})
        return token

    async def register(self, user_create: UserCreateSchema) -> UserRegisterSchema:
        """
        Регистрирует нового пользователя и возвращает его вместе с парой токенов
        """
        user_create_dict = user_create.model_dump()
        user_create_dict.pop("password")
        user_create_dict["password_hash"] = get_string_hash(user_create.password)

        try:
            user = await self.user_repository.create(user_create_dict)
        except IntegrityError:
            raise ConflictError from None

        return UserRegisterSchema(
            user=UserReadSchema.model_validate(user, from_attributes=True),
            tokens=TokenReadSchema(
                refresh_token=await self._create_refresh_token(user), access_token=await self._create_access_token(user)
            ),
        )

    async def login(self, user_login: UserLoginSchema) -> TokenReadSchema:
        """
        Получение токена по паролю и почте
        """
        user = await self.user_repository.get_by_email(user_login.email)
        if user is None:
            raise NotFoundError

        if not verify_hash(user_login.password, user.password_hash):
            raise AccessError

        return TokenReadSchema(
            refresh_token=await self._create_refresh_token(user), access_token=await self._create_access_token(user)
        )

    async def refresh_token(self, refresh_token: str) -> TokenReadSchema:
        """
        Обновление токена, возвращает новую пару токенов
        """
        payload = verify_token(refresh_token)
        if payload is None or payload.type != "refresh":
            raise AccessError

        user = await self.user_repository.get_by_email(payload.sub)
        token_in_db = await self.token_repository.get(payload.id)

        if (not token_in_db) or (not user) or (not verify_hash(refresh_token, token_in_db.token_hash)):
            raise AccessError

        await self.token_repository.delete(token_in_db)

        return TokenReadSchema(
            refresh_token=await self._create_refresh_token(user),
            access_token=await self._create_access_token(user),
        )

    async def get_user_by_access_token(self, access_token: str) -> User:
        """
        Получение пользователя по токену (для зависимости)
        """
        payload = verify_token(access_token)
        if payload is None or payload.type != "access":
            raise AccessError

        return await self.user_repository.get_by_email(payload.sub)


async def get_user_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    token_repository: Annotated[TokenRepository, Depends(get_token_repository)],
) -> UserService:
    return UserService(user_repository, token_repository)
