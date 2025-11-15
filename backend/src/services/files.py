import uuid
from typing import Annotated

from aiobotocore.client import AioBaseClient
from fastapi import Depends

from src.core.s3.dependencies import get_s3_client
from src.schemas.files import FileDownloadUrlsSchema, FileUploadUrlSchema
from src.settings import settings


class FileService:
    def __init__(self, s3_client: AioBaseClient) -> None:
        self.s3_client = s3_client

    async def _get_presigned_url(self, operation_type: str, key: str) -> str:
        url = await self.s3_client.generate_presigned_url(
            operation_type,
            Params={"Bucket": settings.MINIO_BUCKET, "Key": key},
            ExpiresIn=3600,
        )

        return url.replace(settings.MINIO_HOST, settings.HOST_NAME, 1)

    async def get_upload_url(self, filename: str) -> FileUploadUrlSchema:
        key = f"{uuid.uuid4()!s}_{filename}"
        url = await self._get_presigned_url("put_object", key)
        return FileUploadUrlSchema(key=key, url=url)

    async def get_download_urls(self, keys: list[str]) -> FileDownloadUrlsSchema:
        data = []

        for key in keys:
            url = await self._get_presigned_url("get_object", key)
            data.append(FileUploadUrlSchema(key=key, url=url))

        return FileDownloadUrlsSchema(urls=data)


async def get_file_service(s3_client: Annotated[AioBaseClient, Depends(get_s3_client)]) -> FileService:
    return FileService(s3_client)
