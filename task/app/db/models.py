import datetime

from sqlalchemy import BigInteger, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class User(Base):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    username: Mapped[str]
    password: Mapped[str]
    age: Mapped[int]
    email: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, default=func.now())
