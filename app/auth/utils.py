from datetime import datetime, timedelta
import json
from typing import Optional
from passlib.exc import UnknownHashError

from fastapi.exceptions import HTTPException
from fastapi.param_functions import Security
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy import select
from starlette import status
from .status_codes import TOKEN_EXPIRED
from app.auth.models import User
from app.auth.schema.common import AuthUserSchema, UserTokenPayloadSchema
from core.config import settings
from core.database import DBClient

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return PWD_CONTEXT.verify(plain_password, hashed_password)
    except UnknownHashError:
        return False


def get_password_hash(password: str) -> str:
    return PWD_CONTEXT.hash(password)


async def authenticate(
    *, email: EmailStr, password: str, db: DBClient
) -> Optional[User]:
    users = await db.execute(select(User).filter(User.email == email))
    user = users.scalars().first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(*, sub: UserTokenPayloadSchema) -> str:
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )


def create_refresh_token(*, sub: UserTokenPayloadSchema) -> str:
    return _create_token(
        token_type="refresh_token",
        lifetime=timedelta(hours=settings.REFRESH_TOKEN_EXPIRE_HOURS),
        sub=sub,
    )


def _create_token(
    token_type: str, lifetime: timedelta, sub: UserTokenPayloadSchema
) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type
    payload["exp"] = expire
    payload["iat"] = datetime.utcnow()
    payload["sub"] = json.dumps(sub.dict())

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def create_from_refresh_token(token: str) -> str:
    try:
        payload = jwt.decode(
            token=token, key=settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        if payload and payload["type"] == "refresh_token":
            return create_access_token(
                sub=UserTokenPayloadSchema(**json.loads(payload["sub"]))
            ), create_refresh_token(
                sub=UserTokenPayloadSchema(**json.loads(payload["sub"]))
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


async def request_user(
    auth_info: HTTPAuthorizationCredentials = Security(security),
) -> AuthUserSchema:
    try:
        payload = jwt.decode(
            auth_info.credentials,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_aud": False},
        )
        user = UserTokenPayloadSchema(**json.loads(payload["sub"]))
    except JWTError:
        if auth_info and auth_info.credentials:
            raise HTTPException(
                detail="Signature Expired.",
                status_code=TOKEN_EXPIRED,
            )
        raise HTTPException(
            detail="Could not validate credentials.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    if user is None:
        raise HTTPException(
            detail="Could not validate credentials.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    return AuthUserSchema(**user.dict())
