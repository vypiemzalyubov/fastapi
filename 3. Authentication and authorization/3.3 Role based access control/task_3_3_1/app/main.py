from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.security import authenticate_user, create_jwt_token, has_role, get_permissions
from app.models.user import User

app = FastAPI()


@app.post("/token")
def login(user_in: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    if authenticate_user(user_in.username, user_in.password):
        return {"access_token": create_jwt_token({"sub": user_in.username}), "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.get("/protected_resource")
def get_protected(current_user: User = Depends(has_role({"user"}))) -> dict[str, str]:
    return {
        "message": f"Welcome, {current_user.username}! Access to the resource has been granted"
    }


@app.get("/roles")
def get_role_access(current_user: User = Depends(has_role({"user", "guest"}))) -> dict[str, str]:
    return {
        "message": f"Welcome, {current_user.username}!",
        "role": current_user.role,
        "permissions": get_permissions(current_user.permissions)
    }
