from app.models.user import User


user_data = [User(**{"username": "Hulk Hogan", "password": "strongpass1"}),
             User(**{"username": "Bret Hart", "password": "strongpass2"})]


def get_user_from_db(username: str) -> User | None:
    for user in user_data:
        if user.username == username:
            return user
    return None
