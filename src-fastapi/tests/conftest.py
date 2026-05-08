from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

from database import get_session
from main import app


@pytest_asyncio.fixture()
async def client() -> AsyncGenerator[AsyncClient]:
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    async def override_get_session() -> AsyncGenerator[AsyncSession]:
        async with session_maker() as session:
            yield session

    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)

    app.dependency_overrides[get_session] = override_get_session

    try:
        transport = ASGITransport(app=app, raise_app_exceptions=False)
        async with AsyncClient(
            transport=transport,
            base_url="http://testserver",
        ) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        async with engine.begin() as connection:
            await connection.run_sync(SQLModel.metadata.drop_all)
        await engine.dispose()
