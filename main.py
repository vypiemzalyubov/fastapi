from fastapi import FastAPI

app = FastAPI()


@app.get("/sum/")
def calculate_sum(a: int, b: int):
    return {"result": a + b}
