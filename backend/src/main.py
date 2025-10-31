import logging
from contextlib import asynccontextmanager
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.core.db import init_db
from src.settings import settings
from src.api.router import api_rt


logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # добавьте alembic пж, пока эта затычка
    yield
    # что-то после


def create_app() -> FastAPI:
    app = FastAPI(
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        lifespan=lifespan,
    )

    app.include_router(api_rt)

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = str(round(process_time, 4))
        return response

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.HOST_NAME, "localhost"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = create_app()
