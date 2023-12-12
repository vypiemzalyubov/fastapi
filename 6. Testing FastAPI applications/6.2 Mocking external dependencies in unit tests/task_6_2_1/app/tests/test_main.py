import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app, get_and_process_space_articles


client = TestClient(app)


class TestMain(unittest.TestCase):

    @patch("main.fetch_data_from_api")
    @patch("main.process_data")
    def test_get_and_process_data(self, mock_process_data, mock_fetch_data):
        mock_response = {"key": "value"}
        mock_fetch_data.return_value = mock_response

        mock_processed_data = {"key": "value"}
        mock_process_data.return_value = mock_processed_data

        response = client.get("/snapi_articles/")
        print(response)
        print(response.json())
        
        # Убеждаемся, что fetch_data_from_api был вызван один раз
        mock_fetch_data.assert_called_once()
        # убеждаемся, что process_data был вызван с "mocked response"
        mock_process_data.assert_called_once_with(mock_response)
        # проверяем что status code равен 200
        self.assertEqual(response.status_code, 200)
        # проверяем, что данные ответа соответствуют имитируемым обработанным данным
        self.assertEqual(response.json(), mock_processed_data)
