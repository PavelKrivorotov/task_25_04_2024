from typing import AsyncGenerator

from sqlalchemy import URL
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from app import settings


url = URL.create(
    drivername=f"{settings.DATABASE['MIDDLWARE']}+asyncpg",
    username=settings.DATABASE['USER'],
    password=settings.DATABASE['PASSWORD'],
    database=settings.DATABASE['NAME'],
    host=settings.DATABASE['HOST'],
    port=settings.DATABASE['PORT']
)

engine = create_async_engine(url=url)

async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

