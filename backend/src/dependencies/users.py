from fastapi.params import Depends

from core.dependencies import SessionDep
from services.users import UserService
from repositories.users import UserRepository


async def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session)


async def get_user_service(user_repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository)