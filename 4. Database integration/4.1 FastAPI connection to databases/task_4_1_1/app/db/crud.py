from sqlalchemy.orm import Session
from app.models import models, schemas


def read_todo_db(db: Session, id: int):
    return db.query(models.Todo).filter(models.Todo.id == id).first()


def create_todo_db(db: Session, new_todo: schemas.CreateTodo):
    add_todo = models.Todo(title=new_todo.title,
                           description=new_todo.description,
                           completed=new_todo.completed)
    db.add(add_todo)
    db.commit()
    db.refresh(add_todo)
    return add_todo


def update_todo_db(db: Session, todo_id: int, new_todo: schemas.UpdateTodo):
    update_todo = read_todo_db(db=db, id=todo_id)
    for k, v in new_todo.model_dump().items():
        if k is not None:
            setattr(update_todo, k, v)
    db.commit()
    db.refresh(update_todo)
    return update_todo


def delete_todo_db(db: Session, todo_id: int):
    delete_todo = read_todo_db(db=db, id=todo_id)
    if delete_todo:
        db.delete(delete_todo)
        db.commit()
        return delete_todo
    return None
