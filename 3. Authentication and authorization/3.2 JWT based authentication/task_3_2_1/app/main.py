import jwt
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.models.user import User


app = FastAPI(title="Task 3.2.1")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
EXPIRATION_TIME_SECONDS = 30


USERS_DATA = [
    {"username": "admin", "password": "adminpass"},
    {"username": "Gosling", "password": "goslingpass"}
]


def create_jwt_token(data: dict) -> str:
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")


def get_user(username: str) -> User | None:
    for user in USERS_DATA:
        if user.get("username") == username:
            return user
    return None


def verify_password(password: str, encoded_password: str) -> bool:
    return password == encoded_password


def authenticate_user(username: str, password: str) -> bool:
    db_user = get_user(username)
    if db_user is None or not verify_password(password, db_user.get("password")):
        return False
    return True


def get_exp() -> datetime:
    return datetime.utcnow() + timedelta(seconds=EXPIRATION_TIME_SECONDS)


@app.post("/login")
async def login(user_in: User) -> dict:
    if authenticate_user(user_in.username, user_in.password):
        return {
            "access_token": create_jwt_token({"sub": user_in.username, "exp": get_exp()}),
            "token_type": "bearer"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


@app.get("/protected_resource")
async def get_user(current_user: str = Depends(get_user_from_token)) -> dict:
    db_user = get_user(current_user)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User not found")
    return db_user
