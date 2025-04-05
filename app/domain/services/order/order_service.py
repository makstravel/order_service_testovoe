from typing import List, Dict, Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.models.order import Order
from app.schemas.order import OrderOut
from app.infrastructure.repositories.order_repository import (
    create_order,
    update_order_status,
    get_order_by_id,
    get_orders_by_user_id,
)
from app.domain.services.messaging.rabbitmq_producer import publish_new_order_event
from app.domain.services.cache.redis_cache import (
    get_order_from_cache,
    set_order_to_cache,
    delete_order_cache,
)


async def handle_order_creation(
    db: AsyncSession,
    user_id: int,
    items: List[Dict[str, Any]],
    total_price: float
) -> Order:
    """
    Создает новый заказ в базе данных и публикует событие в очередь RabbitMQ.
    """
    order = await create_order(db, user_id, items, total_price)
    await publish_new_order_event(str(order.id))
    return order


async def get_order_with_cache(
    db: AsyncSession,
    order_id: UUID
) -> Dict[str, Any] | None:
    """
    Получает заказ по ID. Сначала проверяет Redis, при отсутствии — загружает из БД и кэширует.
    """
    # Проверка наличия заказа в кеше
    cached = await get_order_from_cache(str(order_id))
    if cached:
        return cached

    # Получение заказа из БД
    order = await get_order_by_id(db, order_id)
    if not order:
        return None

    # Сериализация и сохранение в кеш
    order_data = OrderOut.model_validate(order).model_dump()
    await set_order_to_cache(str(order_id), order_data)
    return order_data


async def update_order_status_service(
    db: AsyncSession,
    order_id: UUID,
    new_status: str
) -> None:
    """
    Обновляет статус заказа в БД и очищает устаревший кеш.
    """
    await update_order_status(db, order_id, new_status)
    await delete_order_cache(str(order_id))


async def get_user_orders_service(
    db: AsyncSession,
    user_id: int
) -> List[Order]:
    """
    Возвращает список всех заказов, принадлежащих пользователю.
    """
    return await get_orders_by_user_id(db, user_id)
