from fastapi import APIRouter
from fastapi import Depends

from src.schemas.files import FileUploadSchema, FileUrlSchema, FileDownloadSchema
from src.services.files import get_file_service
from src.services.files import FileService


router = APIRouter(prefix="/files")


@router.post(
    "/upload_url",
    response_model=FileUrlSchema,
    tags=["Файлы"]
)
async def get_upload_url(
    file_metadata: FileUploadSchema,
    file_service: FileService = Depends(get_file_service),
):
    url = await file_service.get_upload_url(file_metadata.filename)
    return FileUrlSchema(url=url)


@router.get(
    "/download_url",
    response_model=FileUrlSchema,
    tags=["Файлы"]
)
async def get_download_url(
    file_metadata: FileDownloadSchema,
    file_service: FileService = Depends(get_file_service),
):
    url = await file_service.get_download_url(file_metadata.key)
    return FileUrlSchema(url=url)
