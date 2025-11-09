from aiobotocore.session import get_session
from aiobotocore.client import AioBaseClient

from src.settings import settings

session = get_session()

async def create_s3_client() -> AioBaseClient:
    return session.create_client(
        "s3",
        endpoint_url=settings.MINIO_ENDPOINT,
        aws_secret_access_key=settings.MINIO_ROOT_PASSWORD,
        aws_access_key_id=settings.MINIO_ROOT_USER,
        region_name="us-east-1",
    )


async def init_s3():
    client = await create_s3_client()
    try:
        buckets = await client.list_buckets()
        if settings.MINIO_BUCKET not in {b["Name"] for b in buckets["Buckets"]}:
            await client.create_bucket(Bucket=settings.MINIO_BUCKET)
    finally:
        await client.close()