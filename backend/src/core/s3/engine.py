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
    async with (await create_s3_client()) as client:
        response = await client.list_buckets()
        bucket_names = {b["Name"] for b in response.get("Buckets", [])}

        if settings.MINIO_BUCKET not in bucket_names:
            await client.create_bucket(Bucket=settings.MINIO_BUCKET)