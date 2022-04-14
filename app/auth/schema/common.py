from pydantic import BaseModel


class AuthUserSchema(BaseModel):
    id: str
    email: str
    name: str


class UserTokenPayloadSchema(BaseModel):
    id: str
    email: str
    name: str
