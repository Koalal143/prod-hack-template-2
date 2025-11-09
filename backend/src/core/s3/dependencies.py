from typing import AsyncGenerator

from aiobotocore.client import AioBaseClient

from src.core.s3.engine import create_s3_client


async def get_s3_client() -> AsyncGenerator[AioBaseClient]:
    client = await create_s3_client()
    try:
        yield client
    finally:
        await client.close()