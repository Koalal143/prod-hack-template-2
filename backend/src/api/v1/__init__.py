from fastapi import APIRouter

from src.api.v1 import files, health, users

v1_router = APIRouter(prefix="/v1")


for module in (users, files, health):
    v1_router.include_router(module.router)
