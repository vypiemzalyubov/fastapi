from databases import Database
from fastapi import HTTPException, status
from app.db.config import settings
from app.models.schemas import UserCreate, UserGet
from fastapi.responses import JSONResponse

database = Database(settings.DATABASE_URL_asyncpg)


class DDL:

    async def create_table():
        query_exist = "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'table_users')"
        table_exist = await database.fetch_one(query=query_exist)
        if table_exist[0]:
            query_drop = ("DROP TABLE table_users")
            try:
                await database.execute(query=query_drop)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to drop table")
        query_create = ("CREATE TABLE table_users (id SERIAL PRIMARY KEY, username VARCHAR(255) NOT NULL, \
                        password VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL)")
        try:
            await database.execute(query=query_create)
            return {"message": "Table table_users was successfully created"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create table"
            )


class CRUD:

    async def create_in_db(user: UserCreate) -> UserGet:
        query = "INSERT INTO table_users (username, password, email) VALUES (:username, :password, :email) RETURNING id"
        values = {"username": user.username,
                  "password": user.password, "email": user.email}
        try:
            user_id = await database.execute(query=query, values=values)
            return UserGet(**user.model_dump(), id=user_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user")

    async def get_from_db(user_id: int) -> UserGet:
        query = "SELECT * FROM table_users WHERE id = :user_id"
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
        query = "DELETE FROM table_users WHERE id = :user_id RETURNING id"
        values = {"user_id": user_id}
        try:
            deleted_user = await database.execute(query=query, values=values)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete user from database")
        if deleted_user:
            return JSONResponse(
                status_code=status.HTTP_204_NO_CONTENT, content="User deleted successfully")
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
