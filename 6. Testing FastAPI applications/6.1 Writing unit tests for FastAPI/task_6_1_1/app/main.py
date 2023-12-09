from fastapi import FastAPI, status
from contextlib import asynccontextmanager
from app.db.database import database, create_table, create_in_db, get_from_db, delete_from_db
from app.models.schemas import UserCreate, UserGet


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    await create_table()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan, title="Task 6.1.1")


@app.post("/users/", response_model=UserGet, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    result = await create_in_db(user)
    return result


@app.get("/users/{user_id}", response_model=UserGet, status_code=status.HTTP_200_OK)
async def get_user(user_id: int):
    result = await get_from_db(user_id)
    return result


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    result = await delete_from_db(user_id)
    return result
