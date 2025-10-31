from fastapi import APIRouter

from src.api.v1 import users

v1_router = APIRouter(prefix="/v1")

for module in (users,):
    v1_router.include_router(module.router)