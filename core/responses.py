from typing import List, Union

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from core.schema import BaseResponseDataSchema


class BaseResponse(JSONResponse):
    def __init__(self, code: int, msg: str, data: Union[List[dict], dict]) -> None:
        data_schema = BaseResponseDataSchema(code=code, msg=msg, data=data)
        super(BaseResponse, self).__init__(
            content=jsonable_encoder(data_schema.dict()), status_code=code
        )
