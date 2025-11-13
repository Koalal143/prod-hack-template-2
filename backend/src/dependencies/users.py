from http.client import HTTPException
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.core.error import AccessError
from src.models.users import User
from src.services.users import UserService, get_user_service


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
    service: Annotated[UserService, Depends(get_user_service)],
) -> User:
    try:
        return await service.get_user_by_access_token(credentials.credentials)
    except AccessError:
        raise HTTPException(status_code=401, detail="Invalid token")
