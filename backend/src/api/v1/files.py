from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi_cache.decorator import cache

from src.schemas.files import FileUploadSchema, FileUploadUrlSchema, FileUrlSchema
from src.services.files import FileService, get_file_service

router = APIRouter(prefix="/files")


@router.post(
    "/upload_url",
    tags=["Файлы"],
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


@router.get(
    "/{key}/download_url",
    tags=["Файлы"],
    responses={
        status.HTTP_200_OK: {"description": "Успешное получение URL-адреса для скачивания файла из S3-хранилища."},
    },
)
@cache(expire=30)
async def get_download_url(
    key: str,
    file_service: Annotated[FileService, Depends(get_file_service)],
) -> FileUrlSchema:
    return await file_service.get_download_url(key)
