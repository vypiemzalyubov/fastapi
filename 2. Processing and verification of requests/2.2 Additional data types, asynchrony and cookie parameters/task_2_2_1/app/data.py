from app.models.user import User

user_data: dict = {"username": "John", "password": "Travolta"}
user_db: list[User] = [User(**user_data)]
sessions: dict = {}
