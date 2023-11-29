from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# from app.db import crud
from app.db.database import get_db, session, engine
from app.models import schemas, models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.post("/todo")
async def create():
    return {"message": "Hello World"}
