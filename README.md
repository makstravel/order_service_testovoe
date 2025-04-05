## 🛒 Тестовое задание Order Service

**Order Service** _— сервис для управления заказами, разработанный с использованием FastAPI, PostgreSQL, Redis, RabbitMQ и Celery+Flower._

## Цель тестового задания

_Разработать сервис управления заказами на FastAPI, поддерживающий аутентификацию, работу с очередями сообщений, кеширование и фоновую обработку задач._

_При создании заказа публикуется событие "new_order" в очередь.
Консьюмер обрабатывает заказ и передает его в Celery.
Если заказ запрашивается повторно то он отдает его из кеша (TTL = 5 минут).
При изменении заказа – обновляется кеш._

### В проекте используется:

**Rate limiting (ограничение частоты запросов)** — механизм защиты API от перегрузки и злоупотреблений, позволяющий контролировать, сколько запросов клиент может делать за определённый промежуток времени.

**CORS (Cross-Origin Resource Sharing)** — механизм безопасности, который контролирует доступ веб-страниц к ресурсам, расположенным на другом домене (или порту). Он предотвращает нежелательные кросс-доменные запросы, что особенно важно при работе с REST API.

Поддерживает авторизацию, кэширование, очереди сообщений и фоновые задачи.

### 📦 Технологии
**FastAPI** — высокопроизводительный веб-фреймворк

**PostgreSQL** — основная реляционная БД

**Redis** — кэш для заказов

**RabbitMQ** — брокер сообщений

**Celery** — обработка фоновых задач

**Docker** + Docker Compose — контейнеризация

**Alembic** — миграции схемы базы данных

### 🚀 Быстрый запуск с Docker
1. Клонируйте репозиторий
```bash
git clone https://github.com/makstravel/order_service_testovoe.git && cd order_service_testovoe
```

2. Создайте файл .env

Заполните переменные окружения в .env:

```env
DB_HOST=...
DB_PORT=...
DB_NAME=...
DB_USER=...
DB_PASSWORD=...

REDIS_HOST=redis
REDIS_PORT=6379
CACHE_TTL_SECONDS=300

RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest

SECRET_KEY=...
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=15

RATE_LIMIT=100/minute
ALLOWED_ORIGINS_RAW=http://localhost,http://127.0.0.1
```


```bash
!!Внутри вложен файл entrypoint.sh он запускает миграции!
```

3. Запустите все сервисы
```bash
docker-compose up --build
```

После запуска сервис будет доступен по адресу:
```
📍 http://localhost:8000
```

### 📘 Swagger-документация
Доступна по адресу:
```bash
📄 http://localhost:8000/docs
```
### 🧪 Полезные команды

**Запустить проект**	
```bash
docker-compose up --build
```

**Остановить проект**
```bash
docker-compose down -v
```

**Применить миграции вручную**
```bash
docker-compose exec web alembic upgrade head
```

**Подключиться к Redis CLI**
```bash
docker-compose exec redis redis-cli
```

**Подключиться к PostgreSQL**
```bash
docker-compose exec db psql -U order_user -d order_db
```

**Проверить логи приложения**
```bash
docker-compose logs -f web
```

**Проверить Celery воркера**
```bash
docker-compose logs -f celery_worker
```

### 🧠 Проверка полного цикла

**Регистрация пользователя:**
POST /register/

**Получение токена:**
POST /token/

**Создание заказа:**
POST /orders/

Передавайте JWT в заголовке Authorization: Bearer <token>

**Получение заказа:**
GET /orders/{order_id}/
Сначала из Redis, затем из БД

**Обновление статуса заказа:**
PATCH /orders/{order_id}/

**Получение всех заказов пользователя:**
GET /orders/user/{user_id}/



