## Task 4.1.1

pass

---

1. Запустить приложение
```python
uvicorn app.main:app --reload
```
2. Сделать тестовый запрос в терминале
```python
curl -X POST \
  'http://127.0.0.1:8000/token' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=admin&password=adminpass'

curl -X GET \
  'http://127.0.0.1:8000/protected_resource' \
  -H 'Authorization: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTcwMTAwMDYxNn0.U1Fz37cbjEah0cVCUhhP-joeU7gzYb7W-CYXGD36Gvg'
```

Посмотреть Swagger: http://localhost:8000/docs