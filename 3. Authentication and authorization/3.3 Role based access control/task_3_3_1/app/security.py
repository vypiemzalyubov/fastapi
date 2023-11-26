import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from secrets import token_urlsafe
from passlib.context import CryptContext
from app.models.user import CRUD, User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

SECRET_KEY = token_urlsafe(16)
ALGORITHM = "HS256"
EXPIRATION_TIME = timedelta(minutes=1)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


USERS_DATA = [
    {"username": "admin", "password": "adminpass", "role": "admin",
        "permissions": f"{CRUD.CREATE.value}, {CRUD.READ.value}, {CRUD.UPDATE.value}, {CRUD.DELETE.value}"},
    {"username": "user", "password": "userpass", "role": "user",
        "permissions": f"{CRUD.READ.value}, {CRUD.UPDATE.value}"},
    {"username": "guest", "password": "guestpass", "role": "guest",
        "permissions": f"{CRUD.READ.value}"}
]


for user in USERS_DATA:
    user["password"] = pwd_context.hash(user["password"])


def authenticate_user(username: str, password: str) -> bool:
    for user in USERS_DATA:
        if user["username"] == username:
            return pwd_context.verify(password, user["password"])
    return False


def get_userdata(username: str):
    for user in USERS_DATA:
        if user["username"] == username:
            return User(**user)
    return None


def create_jwt_token(data: dict):
    data.update({"exp": datetime.utcnow() + EXPIRATION_TIME})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def verify_jwt_token(token: str = Depends(oauth2_scheme)):
    try:
        user = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])["sub"]
        return get_userdata(user)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def check_role(current_user: User = Depends(verify_jwt_token)):
    allowed_roles = {"user", "admin"}
    if current_user.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    return current_user


def get_permissions(current_user: User) -> str:
    for user in USERS_DATA:
        if user["username"] == current_user.username:
            return user["permissions"]
    return None