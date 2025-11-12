from http.client import HTTPException
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.core.security import verify_token
from src.models.users import User
from src.repositories.users import UserRepository, get_user_repository


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
    repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> User:
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(403, "Токен недействителен или истек.")

    return await repo.get_by_email(payload.sub)
