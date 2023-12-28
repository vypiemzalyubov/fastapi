from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Operations(Base):
    __tablename__ = "operation"

    id = Column(Integer, primary_key=True)
    quantity = Column(String)
    figi = Column(String)
    instrument_type = Column(String, nullable=True)
    date = Column(type_=TIMESTAMP(timezone=True))
    type = Column(String)
