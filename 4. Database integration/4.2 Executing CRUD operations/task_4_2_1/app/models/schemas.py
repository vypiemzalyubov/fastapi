from pydantic import BaseModel


class CreateTodo(BaseModel):
    title: str
    description: str
    completed: bool = False


class ReadTodo(CreateTodo):
    id: int


class UpdateTodo(CreateTodo):
    pass
