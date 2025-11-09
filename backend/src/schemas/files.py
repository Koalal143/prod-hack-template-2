from pydantic import BaseModel, HttpUrl


class FileUploadSchema(BaseModel):
    filename: str


class FileDownloadSchema(BaseModel):
    key: str


class FileUrlSchema(BaseModel):
    url: HttpUrl
