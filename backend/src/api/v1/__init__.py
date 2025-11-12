from fastapi import APIRouter

from src.api.v1 import files, users

v1_router = APIRouter(prefix="/v1")


for module in (users, files):
    v1_router.include_router(module.router)
