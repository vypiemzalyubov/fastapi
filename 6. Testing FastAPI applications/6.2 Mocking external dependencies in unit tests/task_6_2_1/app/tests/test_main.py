import unittest
from fastapi.testclient import TestClient
from main import app, fetch_data_from_api, process_data
from unittest.mock import patch

client = TestClient(app)

class TestMain(unittest.TestCase):

    @patch("main.requests.get")
    @patch("main.process_data")
    def test_get_and_process_space_articles(self, mock_process_data, mock_get):
        mock_response = {"key": "value"}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        mock_processed_data = {"KEY": "VALUE"}
        mock_process_data.return_value = mock_processed_data

        response = client.get("/snapi_articles/")
        
        mock_get.assert_called_once_with("https://api.spaceflightnewsapi.net/v4/articles/", params={"limit": None, "offset": None})
        mock_process_data.assert_called_once_with(mock_response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), mock_processed_data)

    @patch("main.requests.get")
    @patch("main.process_data")
    def test_get_and_process_space_articles_by_id(self, mock_process_data, mock_get):
        mock_response = {"key": "value"}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        mock_processed_data = {"KEY": "VALUE"}
        mock_process_data.return_value = mock_processed_data

        response = client.get("/snapi_articles/1")
        
        mock_get.assert_called_once_with("https://api.spaceflightnewsapi.net/v4/articles/1")
        mock_process_data.assert_called_once_with(mock_response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), mock_processed_data)