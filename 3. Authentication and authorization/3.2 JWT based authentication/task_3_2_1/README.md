## Task 3.2.1

Для этой задачи программирования вам необходимо реализовать аутентификацию на основе JWT в приложении FastAPI. Используйте библиотеку `PyJWT` для генерации и проверки токенов.

**Требования**:

1. Создайте **конечную точку** FastAPI `/login`, которая принимает запросы POST с полезной нагрузкой JSON, содержащей поля "имя пользователя" (**user_name**) и "пароль" (**password**). Конечная точка должна аутентифицировать пользователя на основе предоставленных учетных данных.

2. Если учетные данные действительны, **сгенерируйте токен JWT** с соответствующим сроком действия и верните его в ответе.

3. Если учетные данные неверны, верните соответствующий **ответ об ошибке**.

4. Создайте **защищенную** конечную точку FastAPI `/protected_resource`, для которой **требуется аутентификация** с использованием **JWT**. Пользователи должны включать сгенерированный токен в заголовок `Autharization` своих запросов для доступа к этой конечной точке.

5. **Проверьте токен JWT** в заголовке `Autharization` для каждого запроса к `/protected_resource`. Если токен действителен, разрешите доступ к конечной точке и верните ответ, указывающий на успешный доступ.

6. Если токен недействителен, срок действия истек или отсутствует, верните соответствующий **ответ об ошибке**.

*Примечание: Вы можете предположить существование гипотетической функции `authenticate_user(username: str, password: str) -> bool`, которая проверяет предоставленные "имя пользователя" и "пароль" по базе данных пользователя и возвращает `True`, если учетные данные действительны, и `False` в противном случае (или создать заглушку такой функции, которая при помощи модуля **random.choice** возвращает True или False).*

**Пример запроса**:
```python
POST /login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "securepassword123"
}
```
**Пример ответа (200 OK)**:
```python
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}
```
**Пример ответа (401 Unauthorized)**:
```python
{
  "detail": "Invalid credentials"
}
```

**!!!!Примечание: Поскольку это упрощенная задача программирования, крайне важно принять дополнительные меры безопасности и следовать рекомендациям для реальных приложений. Кроме того, обработка токенов, механизмы обновления и отзыв токенов являются важными аспектами, которые необходимо учитывать при создании готовой к работе системы аутентификации!!!!**

---

1. Запустить приложение
```python
uvicorn app.main:app --reload
```
2. Сделать тестовый запрос в терминале
```python
curl -X POST \
  'http://127.0.0.1:8000/login' \
  -H 'Content-Type: application/json' \
  -d '{"username": "Gosling", "password": "goslingpass"}'

curl -X GET \
  'http://127.0.0.1:8000/protected_resource' \
  -H 'Authorization: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJHb3NsaW5nIiwiZXhwIjoxNzAwODk3ODA3fQ.iGl1A1n6pz52lK9YV5cDiQvf8PHqaNLzPyCF61-9nQ4'
```

Посмотреть Swagger: http://localhost:8000/docs