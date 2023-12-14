from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel


app = FastAPI()

# псевдо-бд
fake_users_db = [
    {
        "user_id": 1,
        "username": "user123",
        "password": "secretpassword",
        "email": "user@example.com"
    }
]

# имитируем хранилище сессий
sessions = {}


# модельки
class UserCredentials(BaseModel):
    username: str
    password: str

class UserData(BaseModel):
    user_id: int
    username: str
    email: str


# роуты
@app.post("/login/") # проверяем наличие юзера и возвращаем куки
def login(user_creds: UserCredentials, response: Response):
    for user in fake_users_db:
        if user["username"] == user_creds.username and user["password"] == user_creds.password:
            response.set_cookie(key="session_cookie", value="my_random_cookie")
            sessions[user_creds.username] = "my_random_cookie" # это чисто для демонстрации, если 5 юзеров зайдут, то всем не нужно одинаковые куки ставить
            print(sessions)
            return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/protected_data/", response_model=UserData) # возвращаем данные по кукам, если они валидны
def protected_data(request: Request):
    for username, cookie in sessions.items():
        if request.cookies.get("session_cookie") and cookie == request.cookies.get("session_cookie"):
            user = get_user_by_username(username)
            print(UserData(**user))
            return UserData(**user)
    raise HTTPException(status_code=401, detail="Bad cookie")


def get_user_by_username(username: str): # вспомогательная функция по извлечению юзера из БД
    for user in fake_users_db:
        if user.get("username") == username:
            return user
    else:
        raise HTTPException(status_code=404, detail="User not found")