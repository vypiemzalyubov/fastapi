## Task 2.1.2

Ваша задача - создать приложение FastAPI, которое обрабатывает запросы, связанные с продуктами (товарами). Приложение должно иметь две конечные точки:

1. Конечная точка для получения информации о продукте:
   - Маршрут: `/product/{product_id}`
   - Метод: **GET**
   - Параметр пути:
     - `product_id`: идентификатор продукта (целое число)
   - Ответ: Возвращает объект JSON, содержащий информацию о продукте, основанную на предоставленном `product_id`.

2. Конечная точка для поиска товаров:
   - Маршрут: `/products/search`
   - Метод: **GET**
   - Параметры запроса:
     - `keyword` (строка, обязательна): ключевое слово для поиска товаров.
     - `category` (строка, необязательно): категория для фильтрации товаров.
     - `limit` (целое число, необязательно): максимальное количество товаров для возврата (по умолчанию 10, если не указано иное).
   - Ответ: Возвращает массив JSON, содержащий информацию о продукте, соответствующую критериям поиска.

3. Для примера можете использовать следующие данные с целью последующего направления ответа:
```python
sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}

sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
}

sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
}

sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]
``` 

Пример:

Запрос GET на `/product/123` должен возвращать:
```python
{
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}
```
В ответ на GET-запрос на `/products/search?keyword=phone&category=Electronics&limit=5` должно вернуться:
```python
[
    {
        "product_id": 123,
        "name": "Smartphone",
        "category": "Electronics",
        "price": 599.99
    },
    {
        "product_id": 789,
        "name": "Iphone",
        "category": "Electronics",
        "price": 1299.99
    },
    ...
]
```
Обратите внимание, что если маршруты будут одинаковыми (например, `/products/{product_id`} и `/products/search`), то у нас второй маршрут будет не рабочим, тк слово search FastAPI будет пытаться привести к int, то есть обработать первый маршрут, и выдаст ошибку). Маршруты обрабатываются в порядке объявления хендлеров). 

Пожалуйста, внедрите приложение FastAPI и протестируйте конечные точки с помощью таких инструментов, как "curl", Postman или любой другой клиент API.

---

1. Запустить приложение
```python
uvicorn app.main:app --reload
```
2. Сделать тестовый запрос в терминале
```bash
curl -X 'POST' \
  'http://localhost:8000/create_user' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Alex",
  "email": "alex@example.com",
  "age": 18,
  "is_subscribed": true  
}'
```

Посмотреть Swagger: http://localhost:8000/docs