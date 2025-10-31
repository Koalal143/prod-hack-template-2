from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from src.settings import settings


engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
