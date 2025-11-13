from src.core.db.dependencies import SessionDep
from src.models.tokens import RefreshToken
from src.repositories.base import BaseRepository


class TokenRepository(BaseRepository[RefreshToken]):
    model = RefreshToken


async def get_token_repository(session: SessionDep) -> TokenRepository:
    return TokenRepository(session)