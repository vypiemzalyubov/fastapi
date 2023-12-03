from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.db.config import settings


sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
    pool_size=5,
    max_overflow=10
)


session_factory = sessionmaker(sync_engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = session_factory()
    try:
        yield db
    finally:
        db.close()
