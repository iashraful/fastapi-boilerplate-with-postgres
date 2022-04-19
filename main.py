import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.auth.routes import auth_router, user_router
from core.config import settings
from core.database import get_db
from core.schema import BaseResponseDataSchema

app = FastAPI(title="FastAPI Boilerplate API Documentation")


# Register CORS
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    _error_response = BaseResponseDataSchema(msg=exc.detail, code=exc.status_code)
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_response.dict(),
    )


@app.exception_handler(ValidationError)
async def validation_error_exception_handler(request: Request, exc: ValidationError):
    _error_response = BaseResponseDataSchema(
        msg="Invalid data found.",
        code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        data=exc.errors(),
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=_error_response.dict(),
    )


@app.get("/")
def read_root(db=Depends(get_db)):
    return {"Hello": "World"}


# Includes all the urls here
app.include_router(auth_router, prefix="/api")
app.include_router(user_router, prefix=settings.API_V1_PREFIX)
