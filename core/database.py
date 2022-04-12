from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.config import settings

engine = create_async_engine(settings.DB_CONN_STRING, echo=True)
LocalSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db():
    db = None
    try:
        db = LocalSession()
        yield db
    finally:
        if db:
            db.close()
