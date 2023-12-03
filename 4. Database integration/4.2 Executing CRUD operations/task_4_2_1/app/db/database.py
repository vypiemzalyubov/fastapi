from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.db.config import settings


async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
    pool_size=5,
    max_overflow=10    
)

async_session_factory = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    pass


async def get_db():
    db = async_session_factory()
    try:
        yield db
    finally:
        await db.close()
