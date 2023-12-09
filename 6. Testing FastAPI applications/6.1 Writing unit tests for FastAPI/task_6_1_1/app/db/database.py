from databases import Database
from fastapi import HTTPException, status
from app.db.config import settings
from app.models.schemas import UserCreate, UserGet

database = Database(settings.DATABASE_URL_asyncpg)


async def create_table():
    query_exist = "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'usertable')"
    table_exist = await database.fetch_one(query=query_exist)
    if table_exist[0]:
        query_drop = ("DROP TABLE usertable")
        try:
            await database.execute(query=query_drop)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to drop table")
    query_create = ("CREATE TABLE usertable (id SERIAL PRIMARY KEY, username VARCHAR(255) NOT NULL, \
                     password VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL)")
    try:
        await database.execute(query=query_create)
        return {"message": "Table usertable was successfully created"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create table"
        )


async def create_in_db(user: UserCreate) -> UserGet:
    query = "INSERT INTO usertable (username, password, email) VALUES (:username, :password, :email) RETURNING id"
    values = {"username": user.username,
              "password": user.password, "email": user.email}
    try:
        user_id = await database.execute(query=query, values=values)
        return UserGet(**user.model_dump(), id=user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}Failed to create user")


async def get_from_db(user_id: int) -> UserGet:
    query = "SELECT * FROM usertable WHERE id = :user_id"
    values = {"user_id": user_id}
    try:
        result = await database.fetch_one(query=query, values=values)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Failed to fetch user from database")
    if result:
        return UserGet(id=result["id"], username=result["username"], email=result["email"], password=result["password"])
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


async def delete_from_db(user_id: int):
    query = "DELETE FROM usertable WHERE id = :user_id RETURNING id"
    values = {"user_id": user_id}
    try:
        deleted_rows = await database.execute(query=query, values=values)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete user from database")
    if deleted_rows:
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
