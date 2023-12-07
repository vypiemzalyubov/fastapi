from pydantic import BaseModel, EmailStr, conint, constr


class UserRegister(BaseModel):
    username: str
    age: conint(gt=18)
    password: constr(min_length=4, max_length=8)
    email: EmailStr


class ErrorResponseModel(BaseModel):
    status_code: int
    message: str
    error_code: int
