import secrets
from typing import Literal

from dotenv import load_dotenv
from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../.env",
        case_sensitive=True,
    )

    HOST_NAME: str = "localhost"
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    MODE: Literal["prod", "dev", "test"] = "prod"

    ACCESS_TOKEN_LIFETIME: int = 60 * 60 * 24
    REFRESH_TOKEN_LIFETIME: int = 60 * 60 * 24 * 31

    POSTGRES_USER: str
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432
    POSTGRES_PASSWORD: str

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str

    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_HOST: str
    MINIO_BUCKET: str

    @property
    def minio_endpoint(self) -> str:
        return f"http://{self.MINIO_HOST}:9000"

    @property
    def database_url(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                host=self.POSTGRES_HOST,
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                port=self.POSTGRES_PORT,
                path=f"{self.POSTGRES_DB}",
            )
        )


settings = Settings()
