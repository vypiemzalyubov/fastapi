from pydantic import BaseModel, Field, EmailStr, PositiveInt


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: PositiveInt | None = Field(default=None, lt=150)
    is_subscribed: bool | None = False
