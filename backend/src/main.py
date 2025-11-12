import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.middlewares import ProcessTimeHeaderMiddleware
from src.api.router import api_router
from src.core.cache.engine import connect_to_redis
from src.core.s3.engine import init_s3
from src.settings import settings

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None, None]:
    await connect_to_redis()
    await init_s3()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        openapi_url="/api/openapi.json",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        lifespan=lifespan,
    )

    app.include_router(api_router)

    app.add_middleware(ProcessTimeHeaderMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.HOST_NAME, "localhost"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Process-Time"],
    )

    return app


app = create_app()
