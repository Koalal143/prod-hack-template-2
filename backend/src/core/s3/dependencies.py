from collections.abc import AsyncGenerator

from aiobotocore.client import AioBaseClient

from src.core.s3.engine import create_s3_client


async def get_s3_client() -> AsyncGenerator[AioBaseClient, None]:
    client_context = await create_s3_client()
    async with client_context as client:
        yield client
