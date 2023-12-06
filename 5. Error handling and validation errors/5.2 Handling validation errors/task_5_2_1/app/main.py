from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.models.schemas import User

app = FastAPI(title="Task 5.2.1")

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


@app.post("/exceptions")
async def test_exceptions(user: User):
    return user
