from app.models.schemas import UserRespone


USER_DATA: list[UserRespone] = [UserRespone(**{"username": "John", "age": 60, "email": "fake@mail.com", "password": "strongpass"}), UserRespone(**{
    "username": "Alex", "age": 20, "email": "fake@mail.ru", "password": "strongpasss"})]
sessions: dict = {}


def get_user_from_db(username: str):
    for user in USER_DATA:
        if user.username == username:
            return user
    return None
