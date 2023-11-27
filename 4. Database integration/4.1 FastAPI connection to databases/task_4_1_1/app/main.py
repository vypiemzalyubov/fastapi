from fastapi import FastAPI

app = FastAPI()

app.models.Base.metadata.create_all(bind=app.db.engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}