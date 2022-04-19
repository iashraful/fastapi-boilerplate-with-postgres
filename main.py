from pydantic import ValidationError
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request, status
from core.config import settings
from core.database import get_db
from fastapi.middleware.cors import CORSMiddleware
from app.auth.routes import auth_router, user_router
from core.schema import BaseResponse
from fastapi.responses import JSONResponse

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
    _error_response = BaseResponse(msg=exc.detail, code=exc.status_code)
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_response.dict(),
    )


@app.exception_handler(ValidationError)
async def validation_error_exception_handler(request: Request, exc: ValidationError):
    _error_response = BaseResponse(
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


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, access_log=True)
