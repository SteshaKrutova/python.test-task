Проект представляет собой API для анализа данных устройств. Он включает в себя:
- **API**: RESTful интерфейс для добавления данных и получения аналитики.
- **Worker**: Celery-воркер для обработки задач (например, расчета статистики).
- **База данных**: PostgreSQL для хранения данных.
- **Кэш**: Redis для управления очередями задач Celery.

---

## Содержание
1. [Требования](#требования)
2. [Установка](#установка)
3. [Запуск проекта](#запуск-проекта)
4. [Использование API](#использование-api)
5. [Тестирование](#тестирование)
6. [Структура проекта](#структура-проекта)

---

## Требования

Для работы с проектом необходимы следующие инструменты:
- Python 3.9+
- Docker и Docker Compose
- Git

---

## Установка

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/https://github.com/SteshaKrutova/python.test-task.git
   cd https://github.com/SteshaKrutova/python.test-task.git
   ```

2. **Создайте виртуальное окружение (опционально):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Для Linux/MacOS
   .venv\Scripts\activate     # Для Windows
   ```

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Запуск проекта

1. **Создайте файл `.env`:**
   Создайте файл `.env` в корне проекта и укажите переменные окружения:
   ```
   POSTGRES_USER=user
   POSTGRES_PASSWORD=password
   POSTGRES_DB=mydb
   REDIS_HOST=redis
   REDIS_PORT=6379
   ```

2. **Запустите контейнеры:**
   Используйте Docker Compose для запуска всех сервисов:
   ```bash
   docker-compose up --build
   ```

3. **Проверьте работу API:**
   После запуска API будет доступен по адресу:
   ```
   http://localhost:8000
   ```

---

## Использование API

### Добавление данных устройства
- **Метод**: `POST`
- **URL**: `/api/devices/{device_id}/data`
- **Тело запроса**:
  ```json
  {
    "x": 1.23,
    "y": 4.56,
    "z": 7.89
  }
  ```

### Получение аналитики за период
- **Метод**: `GET`
- **URL**: `/api/devices/{device_id}/analytics?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`
- **Пример ответа**:
  ```json
  {
    "min": {"x": 1.23, "y": 4.56, "z": 7.89},
    "max": {"x": 2.34, "y": 5.67, "z": 8.90},
    "count": 10,
    "sum": {"x": 12.34, "y": 56.78, "z": 89.01},
    "median": {"x": 1.23, "y": 4.56, "z": 7.89}
  }
  ```

---

## Тестирование

1. **Запустите нагрузочное тестирование Locust:**
   Убедитесь, что API запущен, затем выполните:
   ```bash
   locust -f tests/locustfile.py --host=http://localhost:8000
   ```

2. **Откройте интерфейс Locust:**
   Перейдите в браузере по адресу:
   ```
   http://localhost:8089
   ```

3. **Настройте параметры тестирования:**
   - Количество пользователей.
   - Скорость создания пользователей.
   - Время тестирования.

---

## Структура проекта

```
device-analytics/
├── api/                  # Основной код API (FastAPI)
│   ├── main.py           # Главный файл приложения
│   ├── models.py         # Модели SQLAlchemy
│   ├── tasks.py          # Celery-задачи
│   └── database.py       # Настройка подключения к базе данных
├── migrations/           # Миграции Alembic
├── tests/                # Тесты
│   └── locustfile.py     # Нагрузочное тестирование Locust
├── docker-compose.yml    # Конфигурация Docker Compose
├── requirements.txt      # Зависимости Python
└── README.md             # Документация проекта
```

---
