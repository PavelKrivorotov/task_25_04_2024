from typing import AsyncGenerator

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from app import settings


url = URL.create(
    drivername=f"{settings.TEST['DATABASE']['MIDDLWARE']}+asyncpg",
    username=settings.TEST['DATABASE']['USER'],
    password=settings.TEST['DATABASE']['PASSWORD'],
    database=settings.TEST['DATABASE']['NAME'],
    host=settings.TEST['DATABASE']['HOST'],
    port=settings.TEST['DATABASE']['PORT']
)

engine = create_async_engine(url=url)

async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

