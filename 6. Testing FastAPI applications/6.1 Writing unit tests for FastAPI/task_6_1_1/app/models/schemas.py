from pydantic import BaseModel, constr, EmailStr, Field


class UserCreate(BaseModel):
    username: str
    password: constr(min_length=8, max_length=16)
    email: EmailStr


class UserGet(UserCreate):
    id: int
    password: constr(min_length=8, max_length=16) = Field(..., exclude=True)
