from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.crud import SyncCRUD
from app.db.database import get_db
from app.models import schemas


app = FastAPI(title="Task 4.1.1")


@app.on_event("startup")
def create_tables_on_startup():
    SyncCRUD.create_tables()


@app.post("/todos/", status_code=status.HTTP_201_CREATED, response_model=schemas.ReadTodo)
def create_todo(todo: schemas.CreateTodo, db: Session = Depends(get_db)):
    creating_todo = SyncCRUD.create_todo_db(db=db, new_todo=todo)
    return creating_todo


@app.get("/todos/{todo_id}", response_model=schemas.ReadTodo)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    reading_todo = SyncCRUD.read_todo_db(db=db, id=todo_id)
    if reading_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return reading_todo


@app.put("/todos/{todo_id}", response_model=schemas.UpdateTodo)
def update_todo(todo_id: int, new_todo: schemas.UpdateTodo, db: Session = Depends(get_db)):
    updating_todo = SyncCRUD.update_todo_db(
        db=db, todo_id=todo_id, new_todo=new_todo)
    return updating_todo


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    deleting_todo = SyncCRUD.delete_todo_db(db=db, todo_id=todo_id)
    if deleting_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return "Todo successfully deleted"
