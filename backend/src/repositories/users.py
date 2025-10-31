from pydantic import EmailStr

from src.core.db.dependencies import SessionDep
from src.core.repository import BaseRepository
from src.models.users import User

from sqlalchemy import select


class UserRepository(BaseRepository[User]):
    model = User

    async def get_by_email(self, email: EmailStr) -> User | None:
        stmt = select(self.model).where(self.model.email == email)
        result = await self.session.scalars(stmt)
        return result.first()


async def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session)