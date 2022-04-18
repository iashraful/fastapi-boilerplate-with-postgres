from fastapi import HTTPException, status
from pydantic import EmailStr
from app.auth.models import User
from app.auth.schema.v1.user_schema import UserCreateSchema, UserSchema
from app.auth.utils import get_password_hash
from core.database import DBClient
from core.exceptions import DoesNotExistError
from core.orm.repo import BaseSQLAlchemyRepo


class UserRepo(BaseSQLAlchemyRepo):
    def __init__(self, db: DBClient) -> None:
        super(UserRepo, self).__init__(model=User, db=db)

    async def get_by_email(self, email: EmailStr) -> User:
        result = await self.get(filters=(User.email == email,))
        if not result:
            raise DoesNotExistError("User with this email does not exist.")
        return result

    async def create_user(self, user_data: UserCreateSchema) -> UserSchema:
        try:
            user_exist = await self.get_by_email(email=user_data.email)
            if user_exist:
                raise HTTPException(
                    status_code=400, detail="User with this email already exist."
                )
        except DoesNotExistError:
            pass
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
        user: dict = await self.create(data=_user_dict)
        return UserSchema(**user)