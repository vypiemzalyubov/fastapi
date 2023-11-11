from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Numbers(BaseModel):
    num1: int
    num2: int

@app.post("/calculate")
async def calculate(body: Numbers) -> dict[str, int]:
    return {"result": body.num1 + body.num2}