from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.schemas.files import FileUploadSchema, FileUploadUrlSchema, FileUrlSchema
from src.services.files import FileService, get_file_service

router = APIRouter(prefix="/files")


@router.post("/upload_url", tags=["Файлы"])
@cache(expire=30)
async def get_upload_url(
    file_metadata: FileUploadSchema,
    file_service: Annotated[FileService, Depends(get_file_service)],
) -> FileUploadUrlSchema:
    return await file_service.get_upload_url(file_metadata.filename)


@router.get("/{key}/download_url", tags=["Файлы"])
@cache(expire=30)
async def get_download_url(
    key: str,
    file_service: Annotated[FileService, Depends(get_file_service)],
) -> FileUrlSchema:
    return await file_service.get_download_url(key)
