from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from app.auth.models import User
from app.auth.schema.v1.user_schema import UserCreateSchema, UserResponse, UserSchema
from app.auth.utils import get_password_hash, request_user
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

    @staticmethod
    async def create(user_data: UserCreateSchema, db: DBClient = Depends(get_db)):
        user_exist = await db.execute(
            select(User).filter(User.email == user_data.email)
        )
        if user_exist.first():
            raise HTTPException(
                status_code=400, detail="User with this email already exist."
            )
        if user_data.password != user_data.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password and Confirm Password are not matching.",
            )
        _hashed_password = get_password_hash(password=user_data.password)
        _user_dict = user_data.dict()
        del _user_dict["confirm_password"]
        del _user_dict["password"]
        _user_dict["hashed_password"] = _hashed_password
        _user_dict["is_active"] = True
        user = User(**_user_dict)
        db.add(user)
        await db.commit()
        db.refresh(user)
        return UserResponse(
            code=status.HTTP_201_CREATED,
            msg="User created successfully.",
            data=UserSchema(**user.__dict__),
        )
