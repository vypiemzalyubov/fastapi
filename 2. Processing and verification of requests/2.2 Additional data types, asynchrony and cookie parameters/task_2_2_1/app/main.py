from datetime import datetime
from fastapi import FastAPI, Cookie, Response
from app.models.login import Login

app = FastAPI(title="Task 2.2.1")


@app.post("/login")
async def login_user(login: Login, response: Response):
    now = datetime.now()
    token = response.set_cookie(
        key="session_token", value=now, secure=True, httponly=True)
    return token


@app.get("/user")
async def get_user(session_token: str = Cookie(default=None)):
    return {"session_token": session_token}
