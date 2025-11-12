from sqlalchemy.ext.asyncio import create_async_engine

from src.models.base import Base
from src.settings import settings

engine = create_async_engine(settings.database_url, echo=True, future=True)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
