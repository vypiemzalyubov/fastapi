## Task 6.3.1

Для этой задачи программирования вам нужно написать интеграционные тесты, используя "TestClient" для приложения FastAPI с интеграцией с базой данных.

**Требования:**

1. Настройте приложение FastAPI с интеграцией с базой данных (например, SQLite, PostgreSQL или MySQL).

2. Подготовьте тестовую среду, создав отдельную тестовую базу данных. Настройте свое приложение так, чтобы оно использовало эту тестовую базу данных во время интеграционного тестирования.

3. Внедрите по крайней мере три конечные точки API с различными функциональными возможностями, такими как регистрация пользователей, извлечение данных и обновление данных.

4. Напишите интеграционные тесты, используя `pytest` и `TestClient` для тестирования конечных точек API. Убедитесь, что тесты охватывают различные сценарии, включая положительные случаи и сценарии потенциальных ошибок.

5. Протестируйте поведение конечной точки в различных условиях, таких как отправка неверных данных, проверки подлинности и авторизации, а также пограничные случаи.

6. Убедитесь, что интеграционные тесты корректно взаимодействуют с приложением и базой данных, выполняя операции CRUD должным образом.

7. Включите по крайней мере один тест, который проверяет поведение механизмов аутентификации и авторизации в вашем приложении.

*Примечание: Для выполнения этой задачи вы можете использовать подходящий компонент database engine, такой как SQLite или PostgreSQL, для вашей тестовой среды. Не забудьте сбросить тестовую базу данных перед каждым тестированием, чтобы обеспечить "чистый лист" для каждого тестового примера.*

---

1. Запустить приложение
```python
uvicorn app.main:app --reload
```
2. Запустить на localhost базу данных PostgreSQL с именем fastapidb, порт 5432

3. Сделать тестовые запросы в терминале
```python
curl -X 'POST' \
  'http://localhost:8000/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "Dale",
  "password": "dalepass",
  "email": "dale@disney.com"
}'

curl -X 'GET' \
  'http://localhost:8000/users/1' \
  -H 'accept: application/json'

curl -X 'DELETE' \
  'http://localhost:8000/users/1' \
  -H 'accept: */*'
```

4. Запуск тестов
```python
pytest app/tests/test_main.py
```

Посмотреть Swagger: http://localhost:8000/docs