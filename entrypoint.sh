#!/bin/bash
set -e

# Ожидание PostgreSQL
echo "⏳ Ожидание PostgreSQL на $DB_HOST:$DB_PORT..."
until nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 1
done
echo "✅ PostgreSQL доступен."

# Ожидание RabbitMQ
echo "⏳ Ожидание RabbitMQ на $RABBITMQ_HOST:$RABBITMQ_PORT..."
until nc -z "$RABBITMQ_HOST" "$RABBITMQ_PORT"; do
  sleep 1
done
echo "✅ RabbitMQ доступен."

# Ожидание Redis (если используется)
if [[ -n "$REDIS_HOST" && -n "$REDIS_PORT" ]]; then
  echo "⏳ Ожидание Redis на $REDIS_HOST:$REDIS_PORT..."
  until nc -z "$REDIS_HOST" "$REDIS_PORT"; do
    sleep 1
  done
  echo "✅ Redis доступен."
fi

# Применение миграций (только один раз, для API)
if [ "$SERVICE_TYPE" = "api" ]; then
  echo "📦 Применение Alembic миграций..."
  alembic upgrade head
fi

# Запуск нужного сервиса
case "$SERVICE_TYPE" in
  api)
    echo "🚀 Запуск FastAPI приложения..."
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000
    ;;
  worker)
    echo "🚀 Запуск Celery воркера..."
    exec celery -A app.domain.services.tasks.celery_worker worker --loglevel=info
    ;;
  flower)
    echo "🌸 Запуск Flower..."
    exec celery -A app.domain.services.tasks.celery_worker flower --port=5555
    ;;
  *)
    echo "❌ Неизвестный SERVICE_TYPE: $SERVICE_TYPE"
    exit 1
    ;;
esac
