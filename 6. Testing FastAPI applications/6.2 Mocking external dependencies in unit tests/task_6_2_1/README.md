## Task 6.2.1

Для этой задачи программирования вам нужно написать модульные тесты для приложения FastAPI, которое включает в себя имитацию внешних зависимостей.

**Требования:**

1. Настройте приложение FastAPI по крайней мере с двумя конечными точками API, которые взаимодействуют с внешними зависимостями (например, с базой данных или внешним API).

2. Определите внешние функции или API-интерфейсы, которые необходимо имитировать во время модульного тестирования. Создайте план того, какие данные и ответы должны предоставлять эти макеты.

3. Напишите модульные тесты с использованием `pytest` для конечных точек, которые взаимодействуют с внешними зависимостями. Используйте библиотеку `unittest.mock` для создания макетных объектов (заглушек) и исправления внешних функций.

4. Убедитесь, что модульные тесты охватывают различные сценарии и пограничные случаи, включая случаи, когда внешние функции возвращают неожиданные данные или вызывают исключения.

5. Убедитесь, что тестируемый код корректно взаимодействует с имитируемыми внешними зависимостями и соответствующим образом обрабатывает ответы.

6. Следуйте рекомендациям по модульному тестированию и избегайте чрезмерного использования макетов. Разработайте тестируемый код, чтобы модульные тесты были удобными в обслуживании и надежными.

*Примечание: Используйте `unittest.mock.patch` или `unittest.mock.patch.object` для исправления внешних зависимостей в ваших модульных тестах. Фреймворк `pytest` и плагин `pytest-asyncio` рекомендуются для написания асинхронных модульных тестов в FastAPI.*