from pydantic import BaseModel, EmailStr, conint


class UserRegister(BaseModel):
    username: str
    password: str
    age: conint(gt=18)
    email: EmailStr


class UserReturn(BaseModel):
    username: str
    age: int
    email: EmailStr


class ErrorResponseModel(BaseModel):
    status_code: int
    message: str
    error_code: int
