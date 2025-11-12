from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.db.dependencies import get_db_session
from src.main import app
from src.models import Base
from src.settings import Settings


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    return Settings(MODE="test")


@pytest_asyncio.fixture(scope="function")
async def test_engine(test_settings: Settings):
    engine = create_async_engine(
        test_settings.database_url,
        echo=False,
        pool_size=5,
        max_overflow=10,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def test_sessionmaker(test_engine):
    return async_sessionmaker(test_engine, expire_on_commit=False)


@pytest_asyncio.fixture
async def test_session(test_sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    async with test_sessionmaker() as session:
        yield session
        await session.rollback()


def _get_test_db_session(test_sessionmaker):
    async def get_test_db_session() -> AsyncGenerator[AsyncSession, None]:
        async with test_sessionmaker() as session:
            yield session

    return get_test_db_session


@pytest_asyncio.fixture(scope="function")
async def client(test_sessionmaker) -> AsyncGenerator[AsyncClient, None]:
    @asynccontextmanager
    async def empty_lifespan(_):
        yield

    app.dependency_overrides[get_db_session] = _get_test_db_session(test_sessionmaker)
    app.router.lifespan_context = empty_lifespan

    async with (
        LifespanManager(app) as manager,
        AsyncClient(
            transport=ASGITransport(app=manager.app, client=("0.0.0.0", 5732)),
            base_url="http://test",
        ) as c,
    ):
        yield c

    app.dependency_overrides.clear()
