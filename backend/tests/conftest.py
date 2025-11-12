import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator, AsyncIterator

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI

from src.main import app


@asynccontextmanager
async def no_lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield


app.router.lifespan_context = no_lifespan


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with LifespanManager(app) as manager:
        async with AsyncClient(
            transport=ASGITransport(app=manager.app, client=("0.0.0.0", 5732)),
            base_url="http://test",
        ) as c:
            yield c
