from fastapi import FastAPI
from app.models.schemas import Todo
from app.db.database import Base, get_db, session, engine
from app.models import schemas, models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.post("/todo")
async def create():
    return {"message": "Hello World"}
