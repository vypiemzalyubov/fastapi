from fastapi import FastAPI
from app.models.user import User

app = FastAPI()


@app.get("/users", response_model=User)
async def get_user():
    my_user: User = User(name="John Doe", id=1)
    return my_user
