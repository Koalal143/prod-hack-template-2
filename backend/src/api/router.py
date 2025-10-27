from fastapi import APIRouter

from .v1.main_router import v1_router


api_rt = APIRouter(prefix="/api")
api_rt.include_router(v1_router)