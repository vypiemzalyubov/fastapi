from fastapi import FastAPI
from app.models.user_create import UserCreate


app = FastAPI()


@app.post("/create_user")
async def create_user(user: UserCreate):
    pass
