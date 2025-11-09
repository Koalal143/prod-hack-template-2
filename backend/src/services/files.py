import uuid

from aiobotocore.client import AioBaseClient
from fastapi import Depends

from src.core.s3.dependencies import get_s3_client
from src.settings import settings

class FileService:
    def __init__(self, s3_client: AioBaseClient):
        self.s3_client = s3_client

    async def _get_presigned_url(self, operation_type: str, key: str) -> str:
        url = await self.s3_client.generate_presigned_url(
            operation_type,
            Params={
                "Bucket": settings.MINIO_BUCKET,
                "Key": key
            },
            ExpiresIn=3600,
        )

        return url.replace(settings.MINIO_HOST, settings.HOST_NAME, 1)

    async def get_upload_url(self, filename):
        key = f"{str(uuid.uuid4())}_{filename}"
        return await self._get_presigned_url("put_object", key)

    async def get_download_url(self, key: str):
        return await self._get_presigned_url("get_object", key)


async def get_file_service(s3_client: AioBaseClient = Depends(get_s3_client)):
    return FileService(s3_client)