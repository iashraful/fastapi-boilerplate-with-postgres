import uvicorn
from fastapi import Depends, FastAPI
from core.config import settings
from core.database import get_db
from fastapi.middleware.cors import CORSMiddleware
from app.auth.routes import auth_router, user_router

app = FastAPI(title="FastAPI Boilerplate API Documentation")


# Register all the middlewares here
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get("/")
def read_root(db=Depends(get_db)):
    return {"Hello": "World"}


# Includes all the urls here
app.include_router(auth_router, prefix="/api")
app.include_router(user_router, prefix=settings.API_V1_PREFIX)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, access_log=True)
