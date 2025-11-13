import re
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, EmailStr

from src.schemas.tokens import TokenReadSchema


MIN_PASSWORD_LENGTH = 8


def is_correct_password(value: str) -> str:
    if len(value) < MIN_PASSWORD_LENGTH:
        msg = "Пароль должен содержать минимум 8 символов"
        raise ValueError(msg)

    if not re.search(r"[A-Z]", value):
        msg = "Пароль должен содержать хотя бы одну заглавную букву"
        raise ValueError(msg)

    if not re.search(r"[a-z]", value):
        msg = "Пароль должен содержать хотя бы одну строчную букву"
        raise ValueError(msg)

    if not re.search(r"\d", value):
        msg = "Пароль должен содержать хотя бы одну цифру"
        raise ValueError(msg)

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        msg = "Пароль должен содержать хотя бы один специальный символ"
        raise ValueError(msg)

    return value


PasswordStr = Annotated[str, AfterValidator(is_correct_password)]


class UserBaseSchema(BaseModel):
    first_name: str
    second_name: str
    email: EmailStr
    avatar_file_key: str | None = None


class UserCreateSchema(UserBaseSchema):
    password: PasswordStr
    model_config = ConfigDict(from_attributes=True)


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserReadSchema(UserBaseSchema):
    id: int


class UserRegisterSchema(BaseModel):
    user: UserReadSchema
    tokens: TokenReadSchema
