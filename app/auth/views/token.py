from app.auth.schema.common import UserTokenPayloadSchema
from app.auth.schema.token import (
    LoginResponseData,
    RefreshTokenDataSchema,
    RefreshTokenSchema,
    UserLoginSchema,
)
from app.auth.utils import (
    authenticate,
    create_access_token,
    create_from_refresh_token,
    create_refresh_token,
)
from core.database import DBClient, get_db
from core.responses import BaseResponse
from fastapi import Depends, HTTPException, status


class AuthTokenView:
    @staticmethod
    async def auth_token(
        data: UserLoginSchema, db: DBClient = Depends(get_db)
    ) -> BaseResponse:
        user_instance = await authenticate(
            email=data.email, password=data.password, db=db
        )
        if user_instance:
            auth_token = create_access_token(
                sub=UserTokenPayloadSchema(**user_instance.__dict__)
            )
            refresh_token = create_refresh_token(
                sub=UserTokenPayloadSchema(**user_instance.__dict__)
            )
            response_schema = LoginResponseData(
                auth_token=auth_token, refresh_token=refresh_token, token_type="Bearer"
            )
            return BaseResponse(
                code=status.HTTP_200_OK,
                msg="Login successful.",
                data=response_schema,
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Login credentials are wrong.",
        )

    @staticmethod
    async def refresh_token(token: RefreshTokenSchema) -> BaseResponse:
        auth_token, new_refresh_token = create_from_refresh_token(
            token=token.refresh_token
        )

        data = RefreshTokenDataSchema(
            auth_token=auth_token,
            refresh_token=new_refresh_token,
        )
        return BaseResponse(
            msg="Refresh token created successfully.",
            code=status.HTTP_200_OK,
            data=data,
        )
