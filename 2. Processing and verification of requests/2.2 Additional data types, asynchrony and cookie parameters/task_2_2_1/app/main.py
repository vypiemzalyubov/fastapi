from fastapi import FastAPI, Cookie, Response, HTTPException
from app.models.user import User
from app.data import user_db, sessions

app = FastAPI(title="Task 2.2.1")

users = {}


@app.post("/login")
async def login_user(user: User, response: Response):
    for person in user_db:
        if person.username == user.username and person.password == user.password:
            session_token = "fake_token"
            sessions[session_token] = user
            response.set_cookie(key="session_token", value=session_token, httponly=True)
            return {"message": "cookies set"}
        else:
            raise HTTPException(status_code=404, detail="User not found")            


@app.get("/user")
async def get_user(session_token = Cookie()):
    user = sessions.get(session_token)
    if user:
        return user.dict()
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
