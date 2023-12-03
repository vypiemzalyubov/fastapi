from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base, str_256


class Todo(Base):
    __tablename__ = "todo"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str_256]
    description: Mapped[str_256]
    completed: Mapped[bool] = mapped_column(default=False)
