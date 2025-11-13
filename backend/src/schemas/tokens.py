from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: str
    type: str
    id: str | None = None


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class TokenReadSchema(RefreshTokenSchema):
    access_token: str
