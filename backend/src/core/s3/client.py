import os
from aiobotocore.session import get_session
from botocore.client import ClientCreator

from src.settings import settings

session = get_session()

async def get_s3_client() -> ClientCreator:
    return session.create_client(
        "s3",
        endpoint_url=settings.MINIO_ENDPOINT,
        aws_secret_access_key=settings.MINIO_ROOT_USER,
        aws_access_key_id=settings.MINIO_ROOT_PASSWORD,
        region_name="us-east-1"
    )