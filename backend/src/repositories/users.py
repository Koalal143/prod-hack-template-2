from core.repository import BaseRepository
from models.users import User

from sqlalchemy import select

class UserRepository(BaseRepository[User]):
    model = User

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(self.model).where(self.model.email == email)
        result = await self.session.scalars(stmt)
        return result.first()