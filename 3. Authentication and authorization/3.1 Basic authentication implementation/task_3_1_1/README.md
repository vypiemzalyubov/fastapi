## Task 3.1.1

Реализуйте защищенную базовой аутентификацией конечную точку FastAPI `/login`, которая принимает запросы **GET**.

1. Конечная точка должна аутентифицировать пользователя на основе предоставленных учетных данных.

2. Используйте зависимость, чтобы проверить правильность имени пользователя и пароля.

3. Если учетные данные неверны, верните сообщение `HTTPException` с кодом состояния 401 (то же самое возвращается, если учетные данные не предоставлены).

4. Если данные верны, верните секретное сообщение "You got my secret, welcome"

5. Попробуйте сначала авторизоваться с неправильными данными, а потом введите корректные данные. Для получения такой возможности (повторно авторизоваться) изучите информацию про необходимость добавления заголовка `WWW-Authenticate` чтобы браузер снова отображал приглашение для входа в систему.

---

1. Запустить приложение
```python
uvicorn app.main:app --reload
```
2. Сделать тестовый запрос в терминале
```python
curl -X 'GET' \
  'http://localhost:8000/login' \
  -H 'Authorization: Basic SHVsayBIb2dhbjpzdHJvbmdwYXNzMQ==' 
```

Посмотреть Swagger: http://localhost:8000/docs