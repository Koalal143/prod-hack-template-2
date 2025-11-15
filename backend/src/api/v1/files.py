from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi_cache.decorator import cache

from src.dependencies.users import get_current_user
from src.schemas.files import FileDownloadUrlsSchema, FileUploadSchema, FileUploadUrlSchema, KeysSchema
from src.services.files import FileService, get_file_service

router = APIRouter(prefix="/files")


@router.post(
    "/presigned/upload_url",
    tags=["Файлы"],
    description="Получение URL-адреса для загрузки файла в S3-хранилище.",
    dependencies=[Depends(get_current_user)],
    responses={
        status.HTTP_200_OK: {"description": "Успешное получение URL-адреса для загрузки файла в S3-хранилище."},
    },
)
@cache(expire=30)
async def get_upload_url(
    file_metadata: FileUploadSchema,
    file_service: Annotated[FileService, Depends(get_file_service)],
) -> FileUploadUrlSchema:
    return await file_service.get_upload_url(file_metadata.filename)


@router.post(
    "/presigned/download_urls",
    tags=["Файлы"],
    description="Получение URL-адреса/ов для скачивания файла/ов из S3-хранилища.",
    responses={
        status.HTTP_200_OK: {
            "description": "Успешное получение URL-адреса/ов для скачивания файла/ов из S3-хранилища."
        },
    },
)
@cache(expire=30)
async def get_download_urls(
    keys_data: KeysSchema,
    file_service: Annotated[FileService, Depends(get_file_service)],
) -> FileDownloadUrlsSchema:
    return await file_service.get_download_urls(keys_data.keys)
