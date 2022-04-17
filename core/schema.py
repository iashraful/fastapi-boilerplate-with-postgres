from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel


class BaseResponse(BaseModel):
    code: int
    msg: str
    data: Optional[Any]


class BaseCreateSchema(BaseModel):
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class BaseUpdateSchema(BaseModel):
    updated_at: datetime = datetime.now()


class DateTimeShema(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
