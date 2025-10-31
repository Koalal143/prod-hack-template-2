from typing import Annotated

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)
from fastapi import Depends

from src.core.db import engine


async def get_db_session() -> AsyncSession:
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_db_session)]
