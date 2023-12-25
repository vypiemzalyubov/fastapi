import datetime

from pydantic import BaseModel, conint, constr, EmailStr


class UserCreate(BaseModel):
    username: str
    password: constr(min_length=8, max_length=16)
    age: conint(gt=18)
    email: EmailStr


class UserFromDB(UserCreate):
    id: int
    password: str
    created_at: datetime.datetime
