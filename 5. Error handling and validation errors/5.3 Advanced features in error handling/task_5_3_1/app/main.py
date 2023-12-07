from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.models.schemas import UserRegister, ErrorResponseModel


app = FastAPI(title="Task 5.3.1")

user_list: list[UserRegister] = []


error_template = {
    "username": "Username must be a string",
    "age": "Age must be greater than 18",
    "email": "Invalid email format",
    "password": "Password length must be between 8 and 16",
    "phone": "Invalid phone format"
}


@app.exception_handler(RequestValidationError)
def custom_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    custom_message = []
    for error in errors:
        field = error["loc"][1]
        message = error_template.get(field)
        custom_message.append({"field": field, "message": message})
    return JSONResponse(
        status_code=400,
        content=custom_message
    )


class InvalidUserDataException(HTTPException):
    def __init__(self,
                 status_code: int = status.HTTP_400_BAD_REQUEST,
                 detail: str = "Invalid registration data",
                 headers: dict = {"X-ErrorHandleTime": "My headers"}):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class UserNotFoundException(HTTPException):
    def __init__(self,
                 status_code: int = status.HTTP_404_NOT_FOUND,
                 detail: str = "User not found",
                 headers: dict = {"X-ErrorHandleTime": "My headers"}):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request, exc):
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     return PlainTextResponse("You're too young", status_code=403)


@app.post("/register_user", response_model=UserRegister)
async def register_user(user: UserRegister):
    if "fake" in user.username:
        raise HTTPException(status_code=418, detail="Fake is not welcome here")
    user_list.append(dict(user))
    return user


@app.get("/get_user")
async def get_user(username: str):
    user = [user for user in user_list if username == user["username"]]
    if user:
        return user_list[0]
    else:
        raise UserNotFoundException
