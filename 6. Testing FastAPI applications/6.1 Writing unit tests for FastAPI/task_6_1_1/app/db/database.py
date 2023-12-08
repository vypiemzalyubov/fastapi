from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.db.config import settings


sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True
)


session_factory = sessionmaker(sync_engine)

Base = declarative_base()


def get_db():
    db = session_factory()
    try:
        yield db
    finally:
        db.close()
