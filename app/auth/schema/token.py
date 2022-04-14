from pydantic import BaseModel, EmailStr

from core.schema import BaseResponse


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class RefreshTokenDataSchema(BaseModel):
    auth_token: str
    refresh_token: str


class LoginResponseData(BaseModel):
    auth_token: str
    refresh_token: str
    token_type: str


class LoginResponse(BaseResponse):
    data: LoginResponseData


class RefreshTokenResponse(BaseResponse):
    data: RefreshTokenDataSchema
