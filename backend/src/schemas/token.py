from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: str


class TokenReadSchema(BaseModel):
    access_token: str