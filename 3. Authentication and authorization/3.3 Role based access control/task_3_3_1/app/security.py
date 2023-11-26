import jwt
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from secrets import token_urlsafe
from passlib.context import CryptContext
from app.models.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

SECRET_KEY = token_urlsafe(16)
ALGORITHM = "HS256"
EXPIRATION_TIME = timedelta(minutes=1)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

CRUD = ("create", "read", "update", "delete")
create = 0b1000
read = 0b0100
update = 0b0010
delete = 0b0001


USERS_DATA = [
    {"username": "admin", "password": "adminpass", "role": "admin", "permissions": create | read | update | delete},
    {"username": "user", "password": "userpass", "role": "user", "permissions": read | update},
    {"username": "guest", "password": "guestpass", "role": "guest", "permissions": read}
]

for user in USERS_DATA:
    user["password"] = pwd_context.hash(user["password"])


def get_permissions(value: int) -> str:
    permissions = dict(zip(CRUD, tuple(bin(value)[2:].zfill(4))))
    return ", ".join(k for k, v in permissions.items() if int(v))


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


def has_role(roles: set[str]):
    def role_validator(current_user: User = Depends(verify_jwt_token)):
        roles.add("admin")
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Not enough permissions")
        return current_user
    return role_validator
