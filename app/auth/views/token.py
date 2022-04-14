from fastapi import Depends, HTTPException, status
from app.auth.schema.common import UserTokenPayloadSchema
from app.auth.schema.token import (
    LoginResponse,
    LoginResponseData,
    RefreshTokenDataSchema,
    RefreshTokenResponse,
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


class AuthTokenView:
    @staticmethod
    async def auth_token(
        data: UserLoginSchema, db: DBClient = Depends(get_db)
    ) -> LoginResponse:
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
            return LoginResponse(
                code=status.HTTP_200_OK,
                msg="Login successful.",
                data=response_schema,
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Login credentials are wrong.",
        )

    @staticmethod
    async def refresh_token(token: RefreshTokenSchema) -> RefreshTokenResponse:
        auth_token, new_refresh_token = create_from_refresh_token(
            token=token.refresh_token
        )

        data = RefreshTokenDataSchema(
            auth_token=auth_token,
            refresh_token=new_refresh_token,
        )
        return RefreshTokenResponse(
            msg="Refresh token created successfully.",
            code=status.HTTP_200_OK,
            data=data,
        )
