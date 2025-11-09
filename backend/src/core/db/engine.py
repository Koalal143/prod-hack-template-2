from sqlalchemy.ext.asyncio import create_async_engine

from src.models.base import Base
from src.settings import settings


engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
