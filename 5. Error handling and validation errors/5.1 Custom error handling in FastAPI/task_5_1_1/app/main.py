from typing import Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from app.models.schemas import User, ExceptionResponse


app = FastAPI(title="Task 4.3.1")


class CustomExceptionA(HTTPException):
    def __init__(self, detail: str = "exc_id Not Found", status_code: int = 404) -> None:
        super().__init__(detail=detail, status_code=status_code)


class CustomExceptionB(HTTPException):
    def __init__(self, detail: str = "You Shall Not Pass", status_code: int = 403) -> None:
        super().__init__(detail=detail, status_code=status_code)


@app.exception_handler(CustomExceptionA)
async def custom_exception_handler_a(request: Request, exc: ExceptionResponse) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(CustomExceptionB)
async def custom_exception_handler_b(request: Request, exc: ExceptionResponse) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.get("/f_exception/{exc_id}")
async def first_exception(exc_id: int) -> dict[str, str]:
    if exc_id < 0:
        raise CustomExceptionA
    return {"message": f"{exc_id}, You're God damn right."}


@app.post("/s_exception/")
async def second_exception(user: User) -> dict[str, Any]:
    if user.id == 0 and user.username == "Balrog":
        raise CustomExceptionB
    return {**user.model_dump(), "pass": "OK"}
