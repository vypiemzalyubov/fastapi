## Task 1.1.2

Создайте приложение FastAPI, которое принимает **POST-запрос** к конечной точке (маршруту, адресу странички) `/calculate` с двумя числами (`num1` и `num2`) в качестве входных данных. Приложение должно ответить суммой двух чисел.

Например, запрос на `/calculate` с `num1=5` и `num2=10` должен возвращать `{"result": 15}` в ответе.

---

1. Запустить приложение
```python
uvicorn main:app --reload
```
2. Сделать тестовый запрос в терминале
```bash
curl -X 'POST' \
  'http://localhost:8000/calculate' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "num1": 5,
  "num2": 10
}'
```

Посмотреть Swagger: http://localhost:8000/docs
