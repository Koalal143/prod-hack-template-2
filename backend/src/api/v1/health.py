from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_endpoint() -> dict[str, bool]:
    return {"healthy": True}
