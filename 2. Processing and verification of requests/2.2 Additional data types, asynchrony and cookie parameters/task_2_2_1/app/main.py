from fastapi import FastAPI, Response, HTTPException, Cookie
from app.models.login import Login

app = FastAPI(title="Task 2.2.1")

users = {}


@app.post("/login")
async def login_user(login: Login, response: Response):
    users.setdefault("username", login.username)
    users.setdefault("password", login.password)
    session_token = response.set_cookie(
        key="session_token", value="secret_token", secure=True, httponly=True)
    return session_token


@app.get("/user")
async def get_user(session_token: str = Cookie(default=None)):
    if session_token == "secret_token":
        return users
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
