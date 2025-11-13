from pydantic import EmailStr
from sqlalchemy import select

from src.core.db.dependencies import SessionDep
from src.models.users import User
from src.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User

    async def get_by_email(self, email: EmailStr) -> User | None:
        stmt = select(self.model).where(self.model.email == email)
        result = await self.session.scalars(stmt)
        return result.first()


async def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session)
