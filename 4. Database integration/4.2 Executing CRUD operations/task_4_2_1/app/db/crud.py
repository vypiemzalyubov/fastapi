from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Todo
from app.models.schemas import CreateTodo, ReadTodo, UpdateTodo


class AsyncCRUD:

    @staticmethod
    async def read_todo_db(session: AsyncSession, id: int):
        return await session.query(Todo).filter(Todo.id == id).first()

    @staticmethod
    def create_todo_db(session: AsyncSession, new_todo: CreateTodo):
        add_todo = Todo(
            title=new_todo.title,
            description=new_todo.description,
            completed=new_todo.completed
        )
        session.add(add_todo)
        session.commit()
        # await db.refresh(add_todo)
        return add_todo

    @staticmethod
    async def update_todo_db(session: AsyncSession, todo_id: int, new_todo: UpdateTodo):
        update_todo = AsyncCRUD.read_todo_db(
            session=session,
            id=todo_id
        )
        for k, v in new_todo.model_dump().items():
            if k is not None:
                setattr(update_todo, k, v)
        await session.commit()
        await session.refresh(update_todo)
        return update_todo

    @staticmethod
    async def delete_todo_db(session: AsyncSession, todo_id: int):
        delete_todo = AsyncCRUD.read_todo_db(session=session, id=todo_id)
        if delete_todo:
            session.delete(delete_todo)
            await session.commit()
            return delete_todo
        return None
