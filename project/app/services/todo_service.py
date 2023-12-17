from app.api.schemas.todo import ToDoCreate, ToDoFromDB
from app.utils.unitofwork import IUnitOfWork


class ToDoService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def add_todo(self, todo: ToDoCreate) -> ToDoFromDB:
        todo_dict: dict = todo.model_dump()
        async with self.uow:
            todo_from_db = await self.uow.todo.add_one(todo_dict)
            todo_to_return = ToDoFromDB.model_validate(todo_from_db)
            await self.uow.commit()
            return todo_to_return

    async def get_todos(self) -> list[ToDoFromDB]:
        async with self.uow:
            todos: list = await self.uow.todo.find_all()
            return [ToDoFromDB.model_validate(todo) for todo in todos]
