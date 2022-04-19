from app.auth.repo import UserRepo
from app.auth.schema.v1.user_schema import (
    UserCreateSchema,
    UserResponse,
    UserSchema,
)
from app.auth.utils import request_user
from core.database import DBClient, get_db
from core.exceptions import DoesNotExistError
from core.schema import BaseResponse
from fastapi import Depends, HTTPException, status


class UserView:
    @staticmethod
    async def me(db: DBClient = Depends(get_db), current_user=Depends(request_user)):
        return BaseResponse(
            code=status.HTTP_200_OK,
            msg="Request user fetched successfully.",
            data=current_user,
        )

    @staticmethod
    async def create(user_data: UserCreateSchema, db: DBClient = Depends(get_db)):
        try:
            user_repo = UserRepo(db=db)
            user: UserSchema = await user_repo.create_user(user_data=user_data)
            return UserResponse(
                code=status.HTTP_201_CREATED,
                msg="User created successfully.",
                data=user,
            )
        except DoesNotExistError as err:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=err.__str__()
            )
        except Exception as err:
            raise HTTPException(
                status_code=getattr(
                    err, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
                detail=getattr(err, "detail", err.__str__()),
            )
