from fastapi import APIRouter

from src.api.v1.users import user_rt


v1_router = APIRouter(prefix="/v1")
v1_router.include_router(user_rt)
