from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.models.user import User
from app.data import get_user_from_db


app = FastAPI(title="Task 3.1.1")
security = HTTPBasic()


def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)) -> User:
    user = get_user_from_db(credentials.username)
    if user is None or user.password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={'WWW-Authenticate': 'Basic'}
        )
    return user


@app.get("/login")
def get_protected_resource(user: User = Depends(authenticate_user)) -> dict:
    return {"message": "You got my secret, welcome"}
