from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt
from passlib.hash import pbkdf2_sha256
from pydantic import ValidationError

from src.schemas.tokens import TokenPayload
from src.settings import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pbkdf2_sha256.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pbkdf2_sha256.hash(password)


def create_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
        to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


def verify_token(token: str) -> TokenPayload | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        return TokenPayload(**payload)
    except (JWTError, ValidationError):
        return None
