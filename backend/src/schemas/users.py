import re
from typing import Annotated

from pydantic import BaseModel, EmailStr, ValidationError, \
    AfterValidator


def is_correct_password(value: str) -> str:
    if len(value) < 8:
        raise ValidationError('Пароль должен быть не менее 8 символов.')

    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

    if not re.fullmatch(password_regex, value):
        raise ValidationError(
            'Пароль должен содержать не менее 8 символов,'
            ' включая заглавные и строчные буквы,'
            ' цифры и один из специальных символов (@$!%*?&).'
        )

    return value


PasswordStr = Annotated[str, AfterValidator(is_correct_password)]


class UserCreateSchema(BaseModel):
    first_name: str
    second_name: str
    email: EmailStr
    password: PasswordStr
