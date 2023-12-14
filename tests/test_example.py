from fastapi.testclient import TestClient
from main import app  # тут замените импорт на правильное расположение файла


client = TestClient(app)


def test_login_and_access_data():
    # тестируем точку логина, направляя учетные данные и получая куки
    login_data = {
        "username": "user123",
        "password": "secretpassword"
    }
    response = client.post("/login/", json=login_data)
    assert response.status_code == 200
    assert "set-cookie" in response.headers

    # извлекаем куки из ответа
    cookies = response.cookies
    cookie_value = cookies["session_cookie"]

    # проверяем доступ к получению информации через полученные куки
    headers = {
        "Cookie": f"session_cookie= {cookie_value}"
    }
    response = client.get("/protected_data/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert "username" in data
    assert "email" in data
