from fastapi import APIRouter
from fastapi import Depends
from fastapi_cache.decorator import cache

from src.schemas.files import FileUploadSchema, FileUrlSchema, FileUploadUrlSchema
from src.services.files import get_file_service
from src.services.files import FileService


router = APIRouter(prefix="/files")


@router.post(
    "/upload_url",
    response_model=FileUploadUrlSchema,
    tags=["Файлы"],
    responses={
        200: {"description": "Успешное получение URL-адреса для загрузки файла в S3-хранилище."},
    }
)
@cache(expire=30)
async def get_upload_url(
    file_metadata: FileUploadSchema,
    file_service: FileService = Depends(get_file_service),
):
    return await file_service.get_upload_url(file_metadata.filename)


@router.get(
    "/{key}/download_url",
    response_model=FileUrlSchema,
    tags=["Файлы"],
    responses={
        200: {"description": "Успешное получение URL-адреса для скачивания файла из S3-хранилища."},
    }
)
@cache(expire=30)
async def get_download_url(
    key: str,
    file_service: FileService = Depends(get_file_service),
):
    return await file_service.get_download_url(key)
