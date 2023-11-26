import jwt
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from secrets import token_urlsafe
from passlib.context import CryptContext

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

SECRET_KEY = token_urlsafe(16)
ALGORITHM = "HS256"
EXPIRATION_TIME = timedelta(minutes=5)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# permissions
CRUD = ('create', 'read', 'update', 'delete')
create = 0b1000
read = 0b0100
update = 0b0010
delete = 0b0001

# fake db
USERS_DATA = [
    {'username': 'admin1', 'password': 'adminpass', 'role': 'admin', 'permissions': create | read | update | delete},
    {'username': 'user2', 'password': 'userpass', 'role': 'user', 'permissions': read | update},
    {'username': 'guest3', 'password': 'guestpass', 'role': 'guest', 'permissions': read}
]
for dd in USERS_DATA:
    dd["password"] = pwd_context.hash(dd["password"])

class User(BaseModel):
    username: str
    password: str
    role: str = 'guest'
    permissions: int = 0

def get_permissions(val: int) -> str:
    tmp = dict(zip(CRUD, tuple(bin(val)[2:].zfill(4))))
    return ', '.join(k for k, v in tmp.items() if int(v))

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
        roles.add('admin')
        if current_user.role not in roles:
            raise HTTPException(status_code=401, detail="Insufficient permissions")
        return current_user
    return role_validator

@app.post("/token")
def login(user_in: OAuth2PasswordRequestForm = Depends()):
    if authenticate_user(user_in.username, user_in.password):
        return {"access_token": create_jwt_token({"sub": user_in.username}), "token_type": "bearer"}
    raise HTTPException(
        status_code=401,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

@app.get("/protected_resource")
def get_protected(current_user: User = Depends(has_role({'user'}))):
    return {'message': f'Welcome, {current_user.username}! You have gained access to a protected resource'}

@app.get("/role_based_access")
def get_role_access(current_user: User = Depends(has_role({'user', 'guest'}))):
    return {'message': f'Welcome, {current_user.username}!',
            'role': current_user.role,
            'permissions': get_permissions(current_user.permissions)}