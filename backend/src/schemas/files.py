from pydantic import BaseModel, HttpUrl


class FileUploadSchema(BaseModel):
    filename: str


class FileUrlSchema(BaseModel):
    url: HttpUrl


class FileUploadUrlSchema(FileUrlSchema):
    key: str


class FileDownloadUrlsSchema(BaseModel):
    urls: list[FileUploadUrlSchema]


class KeysSchema(BaseModel):
    keys: list[str]
