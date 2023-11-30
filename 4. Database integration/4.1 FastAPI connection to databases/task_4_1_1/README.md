## Task 4.1.1

Для этой задачи программирования вам необходимо интегрировать FastAPI с базой данных и выполнить базовые операции CRUD с определенным ресурсом.

**Требования**:

1. Выберите любую поддерживаемую базу данных (например, SQLite, PostgreSQL, MySQL или MongoDB) и установите необходимый драйвер базы данных для FastAPI (рекомендуется выбирать ту, с которой больше всего вероятность работать в будущем, либо ту, с которой вы ещё не умеете работать).

2. Создайте **модель данных** (схему) для простого ресурса (например, элемента "Todo" (воображаемый список дел), который включает такие поля, как "id", "title" (заголовок), "description" (описание) и "completed" (завершено).

3. Реализуйте **конечную точку** FastAPI для **создания** нового элемента "Todo". Конечная точка должна принимать POST-запросом полезную нагрузку JSON, содержащую поля "заголовок" и "описание". После успешного создания верните созданный элемент "Todo" в ответе (по умолчанию у нового элемента статус (признак) завершено равен False).

4. Реализуйте конечную точку FastAPI для извлечения одного элемента "Todo" на основе его "id". Конечная точка на **GET-запрос** должна возвращать соответствующий элемент "Todo", если он найден, или соответствующий ответ об ошибке, если элемент не существует.

5. Реализуйте конечную точку FastAPI для **обновления** существующего элемента "Todo" на основе его "id". Конечная точка должна принимать полезную нагрузку JSON (PUT/POST-запрос), содержащую поля "заголовок", "описание" и "завершено". Обновите соответствующий элемент "Todo" в базе данных и верните обновленный элемент в ответе.

6. Реализуйте конечную точку FastAPI для **удаления** элемента "Todo" на основе его "id". Если элемент успешно удален, верните сообщение об успешном завершении в ответе.

Пример POST-запроса create (Создать Todo):
```python
POST /todos
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```
Пример ответа (201 Created):
```python
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false
}
```
Пример GET-запроса read (Получить Todo - ID: 1):
```python
GET /todos/1
```
Пример ответа (200 OK):
```python
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false
}
```

---

1. Запустить приложение
```python
uvicorn app.main:app --reload
```
2. Запустить на localhost базу данных PostgreSQL, порт 5432

3. Сделать тестовые запросы в терминале
```python
curl -X 'POST' \
  'http://localhost:8000/todos/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}'

curl -X 'GET' \
  'http://localhost:8000/todos/1' \
  -H 'accept: application/json'

curl -X 'PUT' \
  'http://localhost:8000/todos/1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "New title",
  "description": "New description"
}'

curl -X 'DELETE' \
  'http://localhost:8000/todos/1' \
  -H 'accept: application/json'
```

Посмотреть Swagger: http://localhost:8000/docs