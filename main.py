from fastapi import FastAPI, Depends
import requests

app = FastAPI()

# Внешний API URL (для демонстрации процесса обратимся сами к себе, но тут должен быть реальный)
EXTERNAL_API_URL = "https://catfact.ninja/fact"


# функция для получения данных из внешнего API
def fetch_data_from_api():
    response = requests.get(EXTERNAL_API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return None


# функция для обработки данных
def process_data(data):
    # как-то логика обработки данных
    new_data = {}
    for key, value in data.items():
        new_data[key.upper()] = value.upper()
    return new_data


# роут, который извлекает и обрабатывает данные от внешнего API
@app.get("/data/")
async def get_and_process_data():
    data: dict = fetch_data_from_api()
    if data:
        return process_data(data)
    else:
        return {"error": "Failed to fetch data from the external API"}