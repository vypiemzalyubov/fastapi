from fastapi import FastAPI
from app.models.user import User, UserAdult

app = FastAPI()


@app.post("/user", response_model=UserAdult)
async def get_user_info(my_user: User):
    response = UserAdult(**my_user.model_dump())
    return response
