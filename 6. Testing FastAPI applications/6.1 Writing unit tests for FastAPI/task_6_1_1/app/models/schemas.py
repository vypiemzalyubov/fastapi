from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    age: int


class UserGet(UserCreate):
    id: int
