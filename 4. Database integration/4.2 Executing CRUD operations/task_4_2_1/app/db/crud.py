from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.models import Todo
from app.models.schemas import CreateTodo, ReadTodo, UpdateTodo


class AsyncCRUD:

    @staticmethod
    async def create_todo_db(session: AsyncSession, new_todo: CreateTodo):
        add_todo = Todo(
            title=new_todo.title,
            description=new_todo.description,
            completed=new_todo.completed
        )
        session.add(add_todo)
        await session.commit()
        return add_todo

    @staticmethod
    async def read_todo_db(session: AsyncSession, id: int):
        return await session.get(Todo, id)

    @staticmethod
    async def update_todo_db(session: AsyncSession, todo_id: int, new_todo: UpdateTodo):
        update_todo = await AsyncCRUD.read_todo_db(
            session=session,
            id=todo_id
        )
        for k, v in new_todo.model_dump().items():
            if k is not None:
                setattr(update_todo, k, v)
        await session.commit()
        return update_todo

    @staticmethod
    async def delete_todo_db(session: AsyncSession, todo_id: int):
        delete_todo = await AsyncCRUD.read_todo_db(session=session, id=todo_id)
        if delete_todo:
            session.delete(delete_todo)
            await session.commit()
            return delete_todo
        return None
