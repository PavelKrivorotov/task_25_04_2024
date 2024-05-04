import asyncio
from typing import Callable, Generator, AsyncGenerator, Any

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils import get_backend_address
from tests.db import async_session_maker


# @pytest.fixture(scope="session")
# def event_loop(request):
#     try:
#         loop = asyncio.get_running_loop()
#     except RuntimeError:
#         loop = asyncio.new_event_loop()
#     yield loop
#     loop.close()


@pytest_asyncio.fixture(scope='session')
# @pytest_asyncio.fixture()
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
        await session.flush()
        await session.rollback()


@pytest.fixture(scope='session')
# @pytest.fixture()
def override_get_async_session(db_session: AsyncSession) -> Callable:
    async def _override_get_async_session():
        yield db_session

    return _override_get_async_session


@pytest.fixture(scope='session')
# @pytest.fixture()
def app(override_get_async_session) -> FastAPI:
    from app.db import get_async_session
    from app.app import app

    app.dependency_overrides[get_async_session] = override_get_async_session
    return app


@pytest_asyncio.fixture(scope='session')
# @pytest_asyncio.fixture()
async def async_client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=get_backend_address()) as client:
        yield client


@pytest.fixture(scope='session')
# @pytest.fixture()
def headers() -> dict[str, Any]:
    return {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

