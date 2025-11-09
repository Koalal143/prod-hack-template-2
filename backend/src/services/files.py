from aiobotocore.client import AioBaseClient

from src.settings import settings

class FileService:
    def __init__(self, s3_client: AioBaseClient):
        self.s3_client = s3_client

    async def _get_presigned_url(self, operation_type: str, key: str):
        return await self.s3_client.generate_presigned_url(
            operation_type,
            Params={
                "Bucket": settings.MINIO_BUCKET,
                "Key": key
            },
            ExpiresIn=3600,
        )

    async def get_upload_url(self, key: str):
        return await self._get_presigned_url("put_object", key)

    async def get_download_url(self, key: str):
        return await self._get_presigned_url("get_object", key)
