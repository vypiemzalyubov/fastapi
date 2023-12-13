from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_item():
    # Отправляем запрос на конечную точку /items/{item_id} с item_id=1
    response = client.get("/items/1")

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"item_id": 1}

    # Отправляем запрос на конечную точку /items/{item_id} с item_id=z (неправильный тип данных)
    response = client.get("/items/z")

    # Assertions
    assert response.status_code == 200  # Это завершится ошибкой, поскольку конечная точка не обработает наш тип данных
    assert response.json() == {"item_id": "z"}  # это тоже завершится ошибкой по той же причине