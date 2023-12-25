from typing import Any, Generator

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_ASYNC_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.ASYNC_DATABASE_URL
    DATABASE_PARAMS = {}

engine = create_async_engine(
    DATABASE_URL,
    **DATABASE_PARAMS,
    echo=False
)

async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


class Base(DeclarativeBase):
    pass


async def get_async_session() -> Generator[AsyncSession, Any, None]:
    async with async_session_maker() as session:
        yield session
