from fastapi import Depends, status
from app.auth.utils import request_user
from core.database import DBClient, get_db
from core.schema import BaseResponse


class UserView:
    @classmethod
    async def me(db: DBClient = Depends(get_db), current_user=Depends(request_user)):
        return BaseResponse(
            code=status.HTTP_200_OK,
            msg="Request user fetched successfully.",
            data=current_user,
        )
