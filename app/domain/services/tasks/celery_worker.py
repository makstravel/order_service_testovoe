import time
from celery import Celery
from app.core.config import settings

# Инициализация экземпляра Celery с настройками брокера (RabbitMQ).
# Этот экземпляр используется для регистрации и выполнения фоновых задач.
celery_app = Celery(
    "order_tasks",
    broker=(
        f"amqp://{settings.rabbitmq_user}:{settings.rabbitmq_password}"
        f"@{settings.rabbitmq_host}:{settings.rabbitmq_port}//"
    ),
)

@celery_app.task
def process_order(order_id: str):
    """
    Фоновая задача обработки заказа.
    """
    time.sleep(2)  # Эмуляция длительной бизнес-операции
    print(f"Order {order_id} processed")
