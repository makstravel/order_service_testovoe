import json
from typing import Optional

import redis.asyncio as redis
from pydantic.json import pydantic_encoder

from app.core.config import settings

# Время жизни кеша (в секундах), берётся из настроек
CACHE_TTL = settings.cache_ttl_seconds

# Инициализация клиента Redis (singleton)
redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    decode_responses=True  # преобразует байты в строки
)


async def get_order_from_cache(order_id: str) -> Optional[dict]:
    """
    Извлекает заказ из Redis по ID, если он есть.

    :param order_id: Идентификатор заказа в виде строки
    :return: Словарь с данными заказа или None
    """
    order_json = await redis_client.get(f"order:{order_id}")
    if order_json:
        return json.loads(order_json)
    return None


async def set_order_to_cache(order_id: str, order_data: dict) -> None:
    """
    Сохраняет заказ в Redis с заданным временем жизни.

    :param order_id: Идентификатор заказа
    :param order_data: Словарь с данными заказа
    """
    await redis_client.set(
        name=f"order:{order_id}",
        value=json.dumps(order_data, default=pydantic_encoder),  # сериализация UUID и datetime
        ex=CACHE_TTL  # TTL в секундах
    )


async def delete_order_cache(order_id: str) -> None:
    """
    Удаляет заказ из Redis-кеша по его ID.

    :param order_id: Идентификатор заказа
    """
    await redis_client.delete(f"order:{order_id}")
