import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Task 4.3.1")


@app.get("/")
async def main():
    return {"message": "Hello"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", host='127.0.0.1', port=8000, reload=True)
