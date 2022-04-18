import asyncio

import pytest
from core.config import settings
from core.database import get_db
from core.model_base import ModelBase
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

loop = asyncio.get_event_loop()


async def create_fresh_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(ModelBase.metadata.drop_all)
        await conn.run_sync(ModelBase.metadata.create_all)


def drop_and_create_db():
    # Creating another engine is not redundency. It's necessary for avoiding the anyio error.
    # RuntimeError: Task <Task pending name='anyio.from_thread.BlockingPortal._call_func' coro=<BlockingPortal._call_func()
    engine = create_engine(url=settings.SYNC_TESTING_DB_CONN_STRING)
    ModelBase.metadata.drop_all(bind=engine)
    ModelBase.metadata.create_all(bind=engine)


def setup_test_db():
    engine = create_async_engine(settings.ASYNC_TESTING_DB_CONN_STRING, echo=True)
    TestAsyncSession = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    drop_and_create_db()
    return TestAsyncSession()


@pytest.fixture()
def session():
    session = setup_test_db()
    yield session


@pytest.fixture()
def client(session):
    async def override_get_db():
        try:
            yield session
        finally:
            print("Closing Connection")
            await session.bind.dispose()
            await session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]


@pytest.fixture()
def auth_token(client):
    user_create_response = client.post(
        "/api/v1/users",
        json={
            "name": "Tester",
            "email": "tester@mail.com",
            "password": "1234",
            "confirm_password": "1234",
        },
    )
    if user_create_response.status_code == 200:
        response = client.post(
            "/api/auth-token", json={"email": "tester@mail.com", "password": "1234"}
        )
        if response.status_code == 200:
            yield response.json()["data"]["auth_token"]
