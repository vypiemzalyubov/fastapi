## Task 1.1

1) Создайте html-файл (напр. "index.html"), в тексте которого напишите:
```html
<!DOCTYPE html>

<html lang="ru">
<head>

<meta charset="UTF-8">

<title> Пример простой страницы html</title>
</head>

<body>

Я НЕРЕАЛЬНО КРУТ И МОЙ РЕСПЕКТ БЕЗ МЕРЫ :)
</body>

</html>
```
2) Создайте приложение FastAPI, которое принимает **GET-запрос** к дефолтной конечной точке (маршруту, адресу странички) ``/`` и возвращает html-страницу.

3) Сохраните файл и запустите приложение с помощью `uvicorn`:
```python
uvicorn main:app --reload
```
Откройте `'http://localhost:8000'` в вашем веб-браузере.

---

1. Запустить приложение
```python
uvicorn main:app --reload
```
2. Открыть http://localhost:8000 в браузере

Посмотреть Swagger: http://localhost:8000/docs
