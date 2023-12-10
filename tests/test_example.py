import unittest
from fastapi.testclient import TestClient
from main import app, fetch_data_from_api, process_data
from unittest.mock import patch

client = TestClient(app)


class TestMain(unittest.TestCase):

    @patch("main.fetch_data_from_api")
    @patch("main.process_data")
    def test_get_and_process_data(self, mock_process_data, mock_fetch_data):
        # Имитируем функцию fetch_data_from_api, чтобы вернуть пример ответа 
        mock_response = {"key": "value"}
        mock_fetch_data.return_value = mock_response

        # имитируем функцию process_data
        mock_processed_data = {"KEY": "VALUE"}
        mock_process_data.return_value = mock_processed_data

        # отправляем запрос на конечную точку /data/ 
        response = client.get("/data/")

        # наши assertions
        mock_fetch_data.assert_called_once()  # Убеждаемся, что fetch_data_from_api был вызван один раз
        mock_process_data.assert_called_once_with(mock_response)  # убеждаемся, что process_data был вызван с "mocked response" 
        self.assertEqual(response.status_code, 200)  # проверяем что status code равен 200
        self.assertEqual(response.json(), mock_processed_data)  # проверяем, что данные ответа соответствуют имитируемым обработанным данным


# from fastapi.testclient import TestClient
# from main import app  # включаем сюда ваш инстанс FastAPI приложения с названием "app"

# # создаём инстанс TestClient для тестирования FastAPI приложения
# client = TestClient(app)


# def test_calculate_sum():
#     # Test case 1: валидные входные данные
#     response = client.get("/sum/?a=5&b=10")
#     assert response.status_code == 200
#     assert response.json() == {"result": 15}

#     # Test case 2: отрицательные числа
#     response = client.get("/sum/?a=-8&b=-3")
#     assert response.status_code == 200
#     assert response.json() == {"result": -11}

#     # Test case 3: ноль и положительное число
#     response = client.get("/sum/?a=0&b=7")
#     assert response.status_code == 200
#     assert response.json() == {"result": 7}

#     # Test case 4: одно число не введено
#     response = client.get("/sum/?a=3")
#     assert response.status_code == 422
#     assert response.json() == {
#         "detail": [
#             {"type": "missing",
#              "loc": ["query", "b"],
#              "msg": "Field required",
#              "input": None,
#              "url": "https://errors.pydantic.dev/2.5/v/missing"}
#         ]
#     }
