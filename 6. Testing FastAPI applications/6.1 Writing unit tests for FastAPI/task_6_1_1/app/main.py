from fastapi import FastAPI, HTTPException
from databases import Database
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# URL для PostgreSQL (измените его под свою БД)
DATABASE_URL = "postgresql://user:password@localhost/dbname"

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
@app.on_event("startup")
async def startup_database():
    await database.connect()

@app.on_event("shutdown")
async def shutdown_database():
    await database.disconnect()
    
    
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

# from fastapi import FastAPI, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from app.db.crud import SyncCRUD
# from app.db.database import get_db
# from app.models.schemas import UserCreate, UserGet


# app = FastAPI(title="Task 6.1.1")


# @app.on_event("startup")
# def create_tables_on_startup():
#     SyncCRUD.create_tables()


# @app.post("/users/", status_code=status.HTTP_201_CREATED, response_model=UserGet)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     creating_user = SyncCRUD.create_user_db(db=db, new_user=user)
#     return creating_user


# @app.get("/users/{user_id}", response_model=UserGet)
# def get_user(user_id: int, db: Session = Depends(get_db)):
#     getting_user = SyncCRUD.read_user_db(db=db, user_id=user_id)
#     if getting_user is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found"
#         )
#     return getting_user


# @app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     deleting_user = SyncCRUD.delete_user_db(db=db, user_id=user_id)
#     if deleting_user is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found"
#         )
#     return "User successfully deleted"
