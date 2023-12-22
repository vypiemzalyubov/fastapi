from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


user_data = {
    "username": "Fake",
    "password": "strongpass",
    "age": 20,
    "email": "fake@example.com"
}


class TestMain:

    created_user_id = None
    updated_user_username = None
    updated_user_password = None

    def test_create_user(self):
        response = client.post("/users/add_user/", json=user_data)
        assert response.status_code == 201
        assert response.json()["username"] == user_data["username"]

        self.__class__.created_user_id = response.json()["id"]

    def test_create_existing_user(self):
        response = client.post("/users/add_user/", json=user_data)
        assert response.status_code == 409

    def test_login(self):
        response = client.post(
            "/auth/login", auth=(user_data.get("username"), user_data.get("password")))
        assert response.status_code == 200
        assert response.json()["username"] == user_data["username"]

    def test_get_all_users(self):
        response = client.get(
            "/users/", auth=(user_data.get("username"), user_data.get("password")))
        assert response.status_code == 200
        assert len(response.json()) > 0

    def test_get_all_users_without_authorization(self):
        response = client.get("/users/")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    def test_change_user(self):
        updated_user_data = {
            "username": "New Fake",
            "password": "newfakepass",
            "age": 21,
            "email": "newsfake@example.com"
        }
        response = client.post(
            f"/users/change_user/?user_id={self.__class__.created_user_id}",
            json=updated_user_data,
            auth=(user_data.get("username"), user_data.get("password")))
        assert response.status_code == 200
        assert response.json()["username"] == updated_user_data["username"]
        assert response.json()["age"] == updated_user_data["age"]
        assert response.json()["email"] == updated_user_data["email"]

        self.__class__.updated_user_username = updated_user_data["username"]
        self.__class__.updated_user_password = updated_user_data["password"]

    def test_delete_non_existing_user(self):
        response = client.delete(
            "/users/999",
            auth=(self.__class__.updated_user_username, self.__class__.updated_user_password))
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    def test_delete_user(self):
        response1 = client.post(
            "/auth/login",
            auth=(self.__class__.updated_user_username, self.__class__.updated_user_password))
        response2 = client.delete(
            f"/users/{self.__class__.created_user_id}",
            auth=(self.__class__.updated_user_username, self.__class__.updated_user_password))
        assert response2.status_code == 204
