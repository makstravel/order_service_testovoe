
import json
import logging

import aio_pika

from app.domain.services.tasks.celery_worker import process_order
from app.core.config import settings

# Инициализация логгера для отслеживания состояния консьюмера
logger = logging.getLogger(__name__)


async def start_consumer():
    """
    Инициализирует асинхронного консьюмера RabbitMQ.

    Подключается к очереди 'orders_queue', слушает входящие сообщения.
    Если сообщение содержит событие 'new_order' — передаёт ID заказа в фоновую задачу Celery.

    Исключения логируются как ошибки с подробностями.
    """
    try:
        # Подключение к RabbitMQ
        connection = await aio_pika.connect_robust(
            host=settings.rabbitmq_host,
            login=settings.rabbitmq_user,
            password=settings.rabbitmq_password
        )
        channel = await connection.channel()

        # Объявление очереди с надёжным сохранением сообщений
        queue = await channel.declare_queue("orders_queue", durable=True)

        logger.info("Consumer успешно подключён к 'orders_queue' и ожидает сообщения.")

        # Асинхронный итератор по сообщениям
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    try:
                        # Десериализация сообщения
                        payload = json.loads(message.body.decode())
                        order_id = payload.get("order_id")
                        event_type = payload.get("event")

                        # Обработка события 'new_order'
                        if event_type == "new_order" and order_id:
                            logger.info(f"Получено событие 'new_order' для заказа: {order_id}")
                            process_order.delay(order_id)
                        else:
                            logger.warning(f"Неизвестное событие или отсутствует order_id: {payload}")

                    except Exception as e:
                        logger.error(f"Ошибка при обработке сообщения: {e}")

    except Exception as conn_err:
        logger.critical(f"Ошибка подключения к RabbitMQ: {conn_err}")
