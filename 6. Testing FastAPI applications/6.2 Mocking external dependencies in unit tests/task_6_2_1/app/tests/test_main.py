import unittest
from fastapi.testclient import TestClient
from main import app, fetch_data_from_api, process_data
from unittest.mock import patch

client = TestClient(app)


class TestMain(unittest.TestCase):

    @patch("main.requests.get")
    @patch("main.process_data")
    def test_get_and_process_space_articles(self, mock_process_data, mock_get):
        mock_response = {
            "count": 18818,
            "next": "https://api.spaceflightnewsapi.net/v4/articles/?limit=1&offset=2",
            "previous": "https://api.spaceflightnewsapi.net/v4/articles/?limit=1",
            "results": [
                {
                    "id": 21835,
                    "title": "NASA will “baby” TEMPO to extend its life",
                    "url": "https://spacenews.com/nasa-will-baby-tempo-to-extend-its-life/",
                    "image_url": "https://i0.wp.com/spacenews.com/wp-content/uploads/2023/12/rsz_screenshot_2023-12-13_at_33414_pm.png",
                    "news_site": "SpaceNews",
                    "summary": "The first NASA satellite to measure air pollution hourly shows so much promise that the space agency is already thinking about ways to extend its life.",
                    "published_at": "2023-12-13T23:49:20Z",
                    "updated_at": "2023-12-13T23:59:15.312000Z",
                    "featured": False,
                    "launches": [],
                    "events": []
                }
            ]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        mock_processed_data = {
            "id": 21835,
            "title": "NASA will “baby” TEMPO to extend its life",
            "url": "https://spacenews.com/nasa-will-baby-tempo-to-extend-its-life/",
            "image_url": "https://i0.wp.com/spacenews.com/wp-content/uploads/2023/12/rsz_screenshot_2023-12-13_at_33414_pm.png",
            "news_site": "SpaceNews",
            "summary": "The first NASA satellite to measure air pollution hourly shows so much promise that the space agency is already thinking about ways to extend its life.",
            "published_at": "2023-12-13T23:49:20Z",
            "updated_at": "2023-12-13T23:59:15.312000Z"
        }
        mock_process_data.return_value = mock_processed_data

        response = client.get("/snapi_articles/?limit=1&offset=1")

        mock_get.assert_called_once_with(
            "https://api.spaceflightnewsapi.net/v4/articles/", params={"limit": 1, "offset": 1})
        mock_process_data.assert_called_once_with(mock_response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), mock_processed_data)

    @patch("main.requests.get")
    @patch("main.process_data")
    def test_get_and_process_space_articles_by_id(self, mock_process_data, mock_get):
        mock_response = {
            "id": 3,
            "title": "Merah Putih Mission",
            "url": "https://www.spacex.com/news/2018/08/06/merah-putih-mission",
            "image_url": "https://www.spacex.com/sites/spacex/files/styles/featured_news_widget_image/public/field/image/merahputihliftoff_0.jpg?itok=KXHDB56L",
            "news_site": "SpaceX",
            "published_at": "2018-08-05T22:00:00Z",
            "updated_at": "2021-05-18T13:43:19.652000Z"
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        mock_processed_data = {
            "title": "Merah Putih Mission",
            "news_site": "SpaceX"
        }
        mock_process_data.return_value = mock_processed_data

        response = client.get("/snapi_articles/3")

        mock_get.assert_called_once_with(
            "https://api.spaceflightnewsapi.net/v4/articles/3")
        mock_process_data.assert_called_once_with(mock_response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), mock_processed_data)
