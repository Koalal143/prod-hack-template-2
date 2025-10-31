from http.client import HTTPException

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.core.auth.security import verify_token
from src.repositories.users import get_user_repository
from src.models.users import User
from src.repositories.users import UserRepository


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    repo: UserRepository = Depends(get_user_repository),
) -> User:
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(403, "Токен недействителен или истек.")

    return await repo.get_by_email(payload.sub)
