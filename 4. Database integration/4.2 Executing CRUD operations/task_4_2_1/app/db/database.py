from databases import Database
from fastapi import HTTPException, status
from app.db.config import settings
from app.models.schemas import CreateTodo, ReturnTodo

database = Database(settings.DATABASE_URL_asyncpg)


async def create_table() -> dict[str, str]:
    query_exist = "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'todo')"
    table_exist = await database.fetch_one(query=query_exist)
    if table_exist[0]:
        query_drop = ("DROP TABLE todo")
        try:
            await database.execute(query=query_drop)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to drop table")
    query_create = ("CREATE TABLE todo (id SERIAL PRIMARY KEY, title VARCHAR(255) NOT NULL,"
                    " description VARCHAR(255) NOT NULL, completed BOOLEAN)")
    try:
        await database.execute(query=query_create)
        return {"message": "Table todo was successfully created"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create table"
        )


async def create_todo_db(todo: CreateTodo) -> ReturnTodo:
    query = "INSERT INTO todo (title, description, completed) VALUES (:title, :description, :completed) RETURNING id"
    values = {"title": todo.title, "description": todo.description,
              "completed": todo.completed}
    try:
        todo_id = await database.execute(query=query, values=values)
        return ReturnTodo(**todo.model_dump(), id=todo_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create todo")


async def get_todo_db(todo_id: int) -> ReturnTodo:
    query = "SELECT * FROM todo WHERE id = :todo_id"
    values = {"todo_id": todo_id}
    try:
        result = await database.fetch_one(query=query, values=values)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Failed to fetch todo from database")
    if result:
        return ReturnTodo(title=result["title"], description=result["description"], id=result["id"])
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")


async def update_todo_db(todo_id: int, todo: CreateTodo):
    query_exist = "SELECT EXISTS(SELECT 1 FROM todo WHERE id = :todo_id)"
    values_exist = {"todo_id": todo_id}
    todo_exist = await database.fetch_val(query=query_exist, values=values_exist)
    if todo_exist:
        query = "UPDATE todo SET title = :title, description = :description WHERE id = :todo_id"
        values = {"todo_id": todo_id,
                  "title": todo.title, "description": todo.description}
        try:
            await database.execute(query=query, values=values)
            return {**todo.model_dump(), "id": todo_id}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update todo in database")
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")


async def delete_todo_db(todo_id: int):
    query = "DELETE FROM todo WHERE id = :todo_id RETURNING id"
    values = {"todo_id": todo_id}
    try:
        deleted_rows = await database.execute(query=query, values=values)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete todo from database")
    if deleted_rows:
        return {"message": "Todo deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
