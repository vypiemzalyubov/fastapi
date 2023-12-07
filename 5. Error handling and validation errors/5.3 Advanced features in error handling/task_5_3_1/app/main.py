from datetime import datetime
from fastapi import FastAPI, Request, Response, Cookie
from fastapi.responses import JSONResponse
from app.models.schemas import UserRegister, ErrorResponseModel
from app.data import USER_DATA, sessions, get_user_from_db
from app.exceptions import UserNotFoundException, InvalidUserCookiesException

app = FastAPI(title="Task 5.3.1")


@app.exception_handler(UserNotFoundException)
async def validation_user_not_found(request: Request, exc: ErrorResponseModel):
    start = datetime.utcnow()
    return JSONResponse(
        status_code=exc.status_code,
        content={"status_code": exc.status_code,
                 "error": "There is no such user here",
                 "solution": exc.solution},
        headers={"X-ErrorHandleTime": str(start - datetime.utcnow())}
    )


@app.exception_handler(InvalidUserCookiesException)
async def validation_user_cookies(request: Request, exc: ErrorResponseModel):
    start = datetime.utcnow()
    return JSONResponse(
        status_code=exc.status_code,
        content={"status_code": exc.status_code,
                 "error": "Oh, authorization failed...",
                 "solution": exc.solution},
        headers={"X-ErrorHandleTime": str(start - datetime.utcnow())}
    )


@app.post("/login")
async def login_user(user: UserRegister, response: Response):
    for person in USER_DATA:
        if person.username == user.username and person.password == user.password:
            session_token = "fake_token"
            sessions[session_token] = get_user_from_db(user.username)
            response.set_cookie(key="session_token",
                                value=session_token, httponly=True)
            return {"message": "cookies set"}
        else:
            raise UserNotFoundException


@app.get("/user")
async def get_user(session_token=Cookie()):
    user = sessions.get(session_token)
    if user:
        return user.dict()
    else:
        raise InvalidUserCookiesException
