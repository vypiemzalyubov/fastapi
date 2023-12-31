## Task 2.2.1

Ваша задача - создать приложение FastAPI, которое реализует аутентификацию на основе файлов cookie. Выполните следующие действия:

1. Создайте простой маршрут входа в систему по адресу `/login`, который принимает имя пользователя и пароль в качестве данных формы. Если учетные данные действительны, установите безопасный файл cookie только для HTTP с именем "session_token" с уникальным значением.

2. Реализуйте защищенный маршрут в `/user`, который требует аутентификации с использованием файла cookie "session_token". Если файл cookie действителен и содержит правильные данные аутентификации, верните ответ в формате JSON с информацией профиля пользователя.

3. Если файл cookie "session_token" отсутствует или недействителен, маршрут `/user` должен возвращать ответ об ошибке с кодом состояния 401 (неавторизован) или сообщение {"message": "Unauthorized"}.

Пример:

POST-запрос в `/login` с данными формы:
```python
{
  "username": "user123"
  "password": "password123"
}
```
Ответ должен содержать файл cookie "session_token".

GET-запрос к `/user` с помощью файла cookie "session_token":
```python
session_token: "abc123xyz456"
```
Ответ должен возвращать информацию профиля пользователя.

GET-запрос к `/user` без файла cookie "session_token" или с недопустимым файлом cookie, например:
```python
session_token: "invalid_token_value"
```
Ответ должен возвращать сообщение об ошибке с кодом состояния 401 или сообщение {"message": "Unauthorized"}.

Пожалуйста, протестируйте свою реализацию с помощью таких инструментов, как "curl", Postman или любой другой клиент API, чтобы проверить функциональность аутентификации на основе файлов cookie.

---

1. Запустить приложение
```python
uvicorn app.main:app --reload
```
2. Сделать тестовый запрос в терминале
```bash
curl -i -X 'POST' \
  'http://localhost:8000/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "John",
  "password": "Travolta"  
}'
```
```python
curl -X 'GET' \
  'http://localhost:8000/user' \
  -H 'accept: application/json' \
  -H 'Cookie: session_token=fake_token'
```

Посмотреть Swagger: http://localhost:8000/docs