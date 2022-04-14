from typing import Any, Optional
from pydantic import BaseModel


class BaseResponse(BaseModel):
    code: int
    msg: str
    data: Optional[Any]
