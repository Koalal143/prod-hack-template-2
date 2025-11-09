from fastapi import APIRouter

from src.schemas.files import FileUploadSchema, FileUrlSchema
from src.services.files import get_file_service
from src.services.files import FileService


router = APIRouter(prefix="/files")


@router.get(
    "/upload_url",
    response_model=FileUrlSchema,
    tags=["Файлы"]
)
async def get_upload_url(
    file_metadata: FileUploadSchema,
    file_service: FileService = get_file_service(),
):
    url = await file_service.get_upload_url(file_metadata.filename)
    return FileUrlSchema(url=url)
