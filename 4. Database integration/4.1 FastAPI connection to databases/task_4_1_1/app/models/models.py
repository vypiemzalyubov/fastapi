from sqlalchemy import Boolean, Column, Integer, String
from app.db.database import Base


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    completed = Column(Boolean, default=False)
