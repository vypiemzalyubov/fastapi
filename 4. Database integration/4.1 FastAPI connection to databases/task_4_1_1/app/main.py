from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import crud
from app.db.database import get_db, session, engine
from app.models import schemas, models


app = FastAPI(title="Task 4.1.1")

models.Base.metadata.create_all(bind=engine)


@app.post("/todos/", status_code=status.HTTP_201_CREATED,response_model=schemas.ReadTodo)
def create_todo(todo: schemas.CreateTodo, db: Session = Depends(get_db)):
    creating_todo = crud.create_todo_db(db=db, new_todo=todo)
    return creating_todo


@app.get("/todos/{todo_id}", response_model=schemas.ReadTodo)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    reading_todo = crud.read_todo_db(db=db, id=todo_id)
    if reading_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return reading_todo


@app.put("/todos/{todo_id}", response_model=schemas.UpdateTodo)
def update_todo(todo_id: int, new_todo: schemas.UpdateTodo, db: Session = Depends(get_db)):
    updating_todo = crud.update_todo_db(
        db=db, todo_id=todo_id, new_todo=new_todo)
    return updating_todo


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    deleting_todo = crud.delete_todo_db(db=db, todo_id=todo_id)
    if deleting_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return "Todo successfully deleted"
