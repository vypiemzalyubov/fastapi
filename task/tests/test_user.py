from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestMain:

    def test_create_user(self):
        user_data = {
            "username": "loluser",
            "password": "testzzzzz",
            "age": 25,
            "email": "test@example.com"
        }
        response = client.post("/users/add_user/", json=user_data)
        assert response.status_code == 201
        # assert response.json()["username"] == user_data["username"]

#     def test_login(self):
#         response = client.post("/login", data={"username": "loser", "password": "testpassword"})
#         assert response.status_code == 200
#         token = response.json()["access_token"]
#         print(token)

    # def test_create_existing_user(self):
    #     user_data = {
    #         "username": "testuser",
    #         "password": "testpassword",
    #         "age": 25,
    #         "email": "test@example.com"
    #     }
    #     response = client.post("/users/add_user/", json=user_data)
    #     assert response.status_code == 409

    # def test_get_all_users(self):
    #     response = client.get(
    #         "/users/", headers={"Authorization": "QTpzdHJpbmdzdA=="})
    #     assert response.status_code == 200
    #     assert len(response.json()) > 0

    # def test_get_user_by_id(self):
    #     response = client.get("/users/1")
    #     assert response.status_code == 200
    #     assert response.json()["id"] == 1

    # def test_update_user(self):
    #     updated_user_data = {
    #         "username": "updated_user",
    #         "password": "updatedpassword",
    #         "age": 30,
    #         "email": "updated@example.com"
    #     }
    #     response = client.post(
    #         "/users/update_user/?user_id=1", json=updated_user_data)
    #     assert response.status_code == 200
    #     assert response.json()["username"] == updated_user_data["username"]
    #     assert response.json()["age"] == updated_user_data["age"]

    # def test_delete_user(self):
    #     response = client.delete("/users/1")
    #     assert response.status_code == 204
