import json
import logging

import aio_pika
from aio_pika import DeliveryMode

from app.core.config import settings

# Инициализация логгера
logger = logging.getLogger(__name__)


async def publish_new_order_event(order_id: str) -> None:
    """
    Публикует событие 'new_order' в очередь RabbitMQ.

    Используется при создании нового заказа для последующей фоновой обработки через Celery.
    """
    try:
        # Устанавливаем асинхронное надёжное соединение с RabbitMQ
        connection = await aio_pika.connect_robust(
            host=settings.rabbitmq_host,
            login=settings.rabbitmq_user,
            password=settings.rabbitmq_password,
        )

        async with connection:
            # Получение канала для обмена сообщениями
            channel = await connection.channel()

            # Убедимся, что очередь существует и устойчива к сбоям
            await channel.declare_queue("orders_queue", durable=True)

            # Формируем и сериализуем сообщение
            message = aio_pika.Message(
                body=json.dumps({
                    "event": "new_order",
                    "order_id": order_id
                }).encode(),
                delivery_mode=DeliveryMode.PERSISTENT  # сохраняется при сбоях брокера
            )

            # Публикуем сообщение в очередь
            await channel.default_exchange.publish(
                message,
                routing_key="orders_queue"
            )

            logger.info(f"Сообщение успешно отправлено: new_order — {order_id}")

    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения в RabbitMQ: {e}")
        raise
