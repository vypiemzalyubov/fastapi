from fastapi import FastAPI
from app.models.user_create import UserCreate


app = FastAPI()

user_list: list[UserCreate] = []


@app.post("/create_user", response_model=UserCreate)
async def create_user(user: UserCreate):
    add_user(user)
    return user


def add_user(user: UserCreate):
    user_list.append(dict(user))
