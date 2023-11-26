from pydantic import BaseModel
from enum import Enum


class CRUD(Enum):
    CREATE: str = "create"
    READ: str = "read"
    UPDATE: str = "update"
    DELETE: str = "delete"


class User(BaseModel):
    username: str
    password: str
    role: str = "guest"
    permissions: str