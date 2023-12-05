from pydantic import BaseModel


class CreateTodo(BaseModel):
    title: str
    description: str
    completed: bool = False


class ReturnTodo(BaseModel):
    id: int
    title: str
    description: str
