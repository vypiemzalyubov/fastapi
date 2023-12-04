from pydantic import BaseModel


class CreateTodo(BaseModel):
    title: str
    description: str


class UpdateTodo(CreateTodo):
    completed: bool = False


class ReadTodo(UpdateTodo):
    id: int
