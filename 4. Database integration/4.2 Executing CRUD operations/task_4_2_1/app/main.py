import asyncio
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.crud import AsyncCRUD
from app.db.database import get_async_session, init_models
from app.models import schemas
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/todos/", status_code=status.HTTP_201_CREATED, response_model=schemas.ReadTodo)
async def create_todo(todo: schemas.CreateTodo, session: AsyncSession = Depends(get_async_session)):
    creating_todo = await AsyncCRUD.create_todo_db(session=session, new_todo=todo)
    return creating_todo


@app.get("/todos/{todo_id}", response_model=schemas.ReadTodo)
async def read_todo(todo_id: int, session: AsyncSession = Depends(get_async_session)):
    reading_todo = await AsyncCRUD.read_todo_db(session=session, id=todo_id)
    if reading_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return reading_todo


@app.put("/todos/{todo_id}", response_model=schemas.UpdateTodo)
async def update_todo(todo_id: int, new_todo: schemas.UpdateTodo, session: AsyncSession = Depends(get_async_session)):
    updating_todo = await AsyncCRUD.update_todo_db(
        session=session, todo_id=todo_id, new_todo=new_todo)
    return updating_todo


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, session: AsyncSession = Depends(get_async_session)):
    deleting_todo = await AsyncCRUD.delete_todo_db(session=session, todo_id=todo_id)
    if deleting_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return "Todo successfully deleted"
