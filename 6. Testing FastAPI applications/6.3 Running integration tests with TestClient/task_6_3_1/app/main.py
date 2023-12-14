from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import database, DDL
from app.router import router as router_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    await DDL.create_table()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan, title="Task 6.1.1")

app.include_router(router_db)
