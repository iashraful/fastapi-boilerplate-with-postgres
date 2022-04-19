from typing import Any
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from core.schema import BaseResponseDataSchema


class BaseResponse(JSONResponse):
    def __init__(self, code: int, msg: str, data: dict) -> None:
        data_schema = BaseResponseDataSchema(code=code, msg=msg, data=data)
        super(BaseResponse, self).__init__(
            content=jsonable_encoder(data_schema.dict()), status_code=code
        )
