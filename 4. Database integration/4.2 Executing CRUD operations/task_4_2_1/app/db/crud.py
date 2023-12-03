from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import Base, async_engine
from app.models.models import Todo
from app.models.schemas import CreateTodo, ReadTodo, UpdateTodo


class AsyncCRUD:

    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def read_todo_db(db: AsyncSession, id: int):
        return await db.query(Todo).filter(Todo.id == id).first()

    @staticmethod
    async def create_todo_db(db: AsyncSession, new_todo: CreateTodo):
        add_todo = Todo(
            title=new_todo.title,
            description=new_todo.description,
            completed=new_todo.completed
        )
        db.add(add_todo)
        await db.commit()
        # await db.refresh(add_todo)
        return add_todo

    @staticmethod
    async def update_todo_db(db: AsyncSession, todo_id: int, new_todo: UpdateTodo):
        update_todo = AsyncCRUD.read_todo_db(
            db=db,
            id=todo_id
        )
        for k, v in new_todo.model_dump().items():
            if k is not None:
                setattr(update_todo, k, v)
        await db.commit()
        await db.refresh(update_todo)
        return update_todo

    @staticmethod
    async def delete_todo_db(db: AsyncSession, todo_id: int):
        delete_todo = AsyncCRUD.read_todo_db(db=db, id=todo_id)
        if delete_todo:
            db.delete(delete_todo)
            await db.commit()
            return delete_todo
        return None
