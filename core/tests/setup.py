import asyncio
import pytest
import sqlalchemy
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.database import get_db
from core.model_base import ModelBase
from main import app
from core.config import settings

event_loop = asyncio.get_event_loop()


async def create_engine():
    engine = create_async_engine(settings.TESTING_DB_CONN_STRING, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(ModelBase.metadata.drop_all)
        await conn.run_sync(ModelBase.metadata.create_all)
    return engine


@pytest.fixture()
def session():
    engine = event_loop.run_until_complete(create_engine())
    connection = event_loop.run_until_complete(engine.connect())
    transaction = connection.begin()
    TestingDBClient = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    session = TestingDBClient(bind=connection)

    # Begin a nested transaction (using SAVEPOINT).
    nested = connection.begin_nested()

    # If the application code calls session.commit, it will end the nested
    # transaction. Need to start a new one when that happens.
    @sqlalchemy.event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    # Rollback the overall transaction, restoring the state before the test ran.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]


@pytest.fixture()
def auth_token(client):
    pass
