import re
from typing import Annotated

from pydantic import BaseModel, EmailStr, ValidationError, AfterValidator


def is_correct_password(value: str) -> str:
    if len(value) < 8:
        raise ValueError("Пароль должен содержать минимум 8 символов")

    if not re.search(r"[A-Z]", value):
        raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")

    if not re.search(r"[a-z]", value):
        raise ValueError("Пароль должен содержать хотя бы одну строчную букву")

    if not re.search(r"\d", value):
        raise ValueError("Пароль должен содержать хотя бы одну цифру")

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValueError("Пароль должен содержать хотя бы один специальный символ")

    return value


PasswordStr = Annotated[str, AfterValidator(is_correct_password)]


class UserBaseSchema(BaseModel):
    first_name: str
    second_name: str
    email: EmailStr


class UserCreateSchema(UserBaseSchema):
    password: PasswordStr

    class Config:
        from_attributes = True


class UserRegisterReadSchema(UserBaseSchema):
    access_token: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserReadSchema(UserBaseSchema):
    id: int
