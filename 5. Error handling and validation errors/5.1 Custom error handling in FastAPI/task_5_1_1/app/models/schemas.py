from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str


class ExceptionResponse(BaseModel):
    error_code: int
    error_message: str
    error_details: str | None = None
