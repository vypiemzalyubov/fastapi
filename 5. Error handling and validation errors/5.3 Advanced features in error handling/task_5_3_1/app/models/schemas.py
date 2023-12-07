from pydantic import BaseModel, EmailStr, conint, constr


class UserRegister(BaseModel):
    username: str
    password: constr(min_length=8, max_length=16)


class UserRespone(UserRegister):
    age: conint(gt=18)
    email: EmailStr


class ErrorResponseModel(BaseModel):
    status_code: int
    message: str
    error_code: int
