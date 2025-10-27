import logging
from contextlib import asynccontextmanager
import time

from fastapi import APIRouter, FastAPI, Request


@asynccontextmanager
async def lifespan(app: FastAPI):
    # что-то до старта
    yield
    # что-то после


def create_main_router():
    router = APIRouter(prefix="/api/v1")
    # router.include_router() подключаем другие роутеры
    return router


app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc")
app.include_router(create_main_router())


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
