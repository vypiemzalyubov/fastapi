import pytest
from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import database, DDL


@pytest.fixture(scope="module")
async def test_db():
    await database.connect()
    await DDL.create_table()
    yield app
    await database.disconnect()


@pytest.fixture(scope="function")
def test_client():
    with TestClient(app) as client:
        yield client


class TestUser:

    @staticmethod
    @pytest.mark.asyncio
    async def test_create_user(test_client):
        user_data = {
            "username": "Zipper",
            "password": "zipperpass",
            "email": "zipper@disney.com"
        }
        response = test_client.post("/users/", json=user_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["username"] == "Zipper"
        assert response.json()["email"] == "zipper@disney.com"
        assert response.json()["id"] == 1

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_data, missing_param", [
        pytest.param({"password": "montypass", "email": "monty@disney.com"},
                     "username", id="missing username"),
        pytest.param({"username": "Chip", "email": "chip@disney.com"},
                     "password", id="missing password"),
        pytest.param({"username": "Dale", "password": "dalepass"},
                     "email", id="missing email")
    ])
    async def test_create_user_without_required_parameters(test_client, user_data, missing_param):
        response = test_client.post("/users/", json=user_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json()["detail"][0]["loc"][1] == missing_param

    @staticmethod
    @pytest.mark.asyncio
    async def test_create_and_get_user(test_client):
        user_data = {
            "username": "Gadget Hackwrench",
            "password": "gadgetpass",
            "email": "gadget@disney.com"
        }
        response1 = test_client.post("/users/", json=user_data)
        assert response1.status_code == status.HTTP_201_CREATED

        user_id = response1.json()["id"]
        response2 = test_client.get(f"/users/{user_id}")
        assert response2.status_code == status.HTTP_200_OK
        assert response2.json()["username"] == "Gadget Hackwrench"
        assert response2.json()["email"] == "gadget@disney.com"

    @staticmethod
    @pytest.mark.asyncio
    async def test_get_missing_user(test_client):
        response = test_client.get("/users/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "User not found"

    @staticmethod
    @pytest.mark.asyncio
    async def test_create_and_delete_user(test_client):
        user_data = {
            "username": "Fat Cat",
            "password": "fatcatpass",
            "email": "fatcat@disney.com"
        }
        response1 = test_client.post("/users/", json=user_data)
        assert response1.status_code == status.HTTP_201_CREATED

        user_id = response1.json()["id"]
        response2 = test_client.delete(f"/users/{user_id}")
        assert response2.status_code == status.HTTP_204_NO_CONTENT

    @staticmethod
    @pytest.mark.asyncio
    async def test_delete_missing_user(test_client):
        response = test_client.delete("/users/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "User not found"
