from pydantic import BaseModel, constr


class User(BaseModel):
    username: str
    password: constr(
        min_length=6,
        max_length=20
    )
