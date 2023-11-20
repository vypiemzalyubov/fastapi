import re
from fastapi import FastAPI, Request, HTTPException

app = FastAPI(title="Task 2.3.1")


@app.get("/headers")
async def get_headers(request: Request) -> dict:
    check_headers(request.headers)
    return {
        "User-Agent": request.headers["user-agent"],
        "Accept-Language": request.headers["accept-language"]
    }


def check_headers(headers: Request.headers):
    if "User-Agent" not in headers:
        raise HTTPException(
            status_code=400,
            detail="Missing required header User-Agent"
        )
    if "Accept-Language" not in headers:
        raise HTTPException(
            status_code=400,
            detail="Missing required header Accept-Language"
        )    
    if not re.fullmatch(r"[A-z\d*,-.;= ]+", headers["Accept-Language"]):
        raise HTTPException(
            status_code=400, 
            detail="Invalid Accept-Language header format"
        )
