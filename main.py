from fastapi import FastAPI, HTTPException
from databases import Database
from sqlalchemy import String, create_engine
from pydantic import BaseModel
from typing import Optional
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

# URL для PostgreSQL (измените его под свою БД)
DATABASE_URL = "postgresql://postgres:password@localhost:5432/postgres"

database = Database(DATABASE_URL)


# Модель User для валидации входных данных
class UserCreate(BaseModel):
    username: str
    email: str


# Модель User для валидации исходящих данных - чисто для демонстрации (обычно входная модель шире чем выходная, т.к. на вход мы просим, например, пароль, который обратно не возвращаем, и другое, что не обязательно возвращать) 
class UserReturn(BaseModel):
    username: str
    email: str
    id: Optional[int] = None


# тут устанавливаем условия подключения к базе данных и отключения - можно использовать в роутах контекстный менеджер async with Database(...) as db: etc
# @app.on_event("startup")
# async def startup_database():
#     await database.connect()

# @app.on_event("shutdown")
# async def shutdown_database():
#     await database.disconnect()
    
    
# создание роута для создания юзеров
@app.post("/users/", response_model=UserReturn)
async def create_user(user: UserCreate):
    query = "INSERT INTO users (username, email) VALUES (:username, :email) RETURNING id"
    values = {"username": user.username, "email": user.email}
    try:
        user_id = await database.execute(query=query, values=values)
        return {**user.dict(), "id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create user")