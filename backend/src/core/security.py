from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt
from passlib.hash import pbkdf2_sha256
from pydantic import ValidationError

from src.schemas.tokens import TokenPayload
from src.settings import settings


def verify_hash(plain_string: str, hashed_string: str) -> bool:
    return pbkdf2_sha256.verify(plain_string, hashed_string)


def get_string_hash(string: str) -> str:
    return pbkdf2_sha256.hash(string)


def create_token(data: dict, expires_delta: timedelta, token_type: str) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
        to_encode.update({"exp": expire, "type": token_type})

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


def verify_token(token: str) -> TokenPayload | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        return TokenPayload(**payload)
    except (JWTError, ValidationError):
        return None
