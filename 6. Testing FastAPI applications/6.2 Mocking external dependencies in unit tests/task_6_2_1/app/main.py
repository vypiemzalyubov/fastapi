from fastapi import FastAPI
import requests

app = FastAPI()


EXTERNAL_API_URL = "https://api.spaceflightnewsapi.net/v4"


def fetch_data_from_api(endpoint: str,
                        id: int = None,
                        limit: int = None,
                        offset: int = None):
    if id:
        response = requests.get(f"{EXTERNAL_API_URL}/{endpoint}/{id}")
        if response.status_code == 200:
            return response.json()
        else:
            return None
    else:
        params = {"limit": limit, "offset": offset}
        response = requests.get(
            f"{EXTERNAL_API_URL}/{endpoint}/", params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None


def process_data(data):
    new_data = {}
    if "results" in data.keys():
        for result in data["results"]:
            for key, value in result.items():
                if result[key]:
                    new_data[key] = value
    else:
        for key, value in data.items():
            if key in ("title", "news_site"):
                new_data[key] = value
    return new_data


@app.get("/snapi_articles/")
async def get_and_process_space_articles(limit: int = None, offset: int = None):
    data: dict = fetch_data_from_api(
        endpoint="articles", limit=limit, offset=offset)
    if data:
        return process_data(data)
    else:
        return {"error": "Failed to fetch data from the Spaceflight News API"}


@app.get("/snapi_articles/{id}")
async def get_and_process_space_articles_by_id(id: int):
    data: dict = fetch_data_from_api(endpoint="articles", id=id)
    if data:
        return process_data(data)
    else:
        return {"error": "Failed to fetch data from the Spaceflight News API"}
