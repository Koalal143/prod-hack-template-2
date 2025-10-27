from datetime import timedelta, datetime, timezone

from passlib.context import CryptContext
from pydantic import ValidationError
from jose import jwt, JWTError

from settings import settings
from schemas.token import TokenPayload

pwd_context = CryptContext(schemes=["bcrypt"])


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_token(data: dict, token_type: str, expires_delta: timedelta) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire, "type": token_type})

    return jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm="HS256"
    )



def verify_token(token: str) -> TokenPayload | None:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"]
        )

        token_data = TokenPayload(**payload)
        return token_data
    except (JWTError, ValidationError):
        return None
