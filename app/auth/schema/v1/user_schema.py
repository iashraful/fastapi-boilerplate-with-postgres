from pydantic import BaseModel, EmailStr

from core.schema import BaseCreateSchema, BaseResponse, DateTimeShema


class UserCreateSchema(BaseCreateSchema):
    name: str
    email: EmailStr
    password: str
    confirm_password: str


class UserSchema(DateTimeShema):
    name: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
    email_verified: bool


class UserResponse(BaseResponse):
    data: UserSchema
