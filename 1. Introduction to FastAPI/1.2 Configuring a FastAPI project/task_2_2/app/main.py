from fastapi import FastAPI
from app.models.user import User

app = FastAPI()


@app.post("/user")
async def get_user_info(user: User):
    user_info = dict(user)
    user_info.update({"is_adult": user_adult(user.age)})
    return user_info


def user_adult(age: int) -> bool:
    return age >= 18
