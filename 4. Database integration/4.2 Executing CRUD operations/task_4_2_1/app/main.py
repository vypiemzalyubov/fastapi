from fastapi import FastAPI, status
from contextlib import asynccontextmanager
from app.db.database import database, create_table, create_todo_db, get_todo_db, update_todo_db, delete_todo_db
from app.models.schemas import CreateTodo, ReturnTodo


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    await create_table()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan, title="Task 4.2.1")


@app.post("/todos/", response_model=ReturnTodo, status_code=status.HTTP_201_CREATED)
async def create(todo: CreateTodo):
    result = await create_todo_db(todo)
    return result


@app.get("/todos/{todo_id}", response_model=ReturnTodo)
async def get_todo(todo_id: int):
    result = await get_todo_db(todo_id)
    return result


@app.put("/todos/{todo_id}", response_model=ReturnTodo)
async def update_todo(todo_id: int, todo: CreateTodo):
    result = await update_todo_db(todo_id, todo)
    return result


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int):
    result = await delete_todo_db(todo_id)
    return result
