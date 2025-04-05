from typing import List, Optional, Dict
from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound

from app.infrastructure.models.order import Order, OrderStatus


async def create_order(
    db: AsyncSession,
    user_id: int,
    items: List[Dict[str, str]],
    total_price: float
) -> Order:
    """
    Создаёт новый заказ и сохраняет его в базе данных.
    """
    # Формирование объекта заказа с автогенерацией UUID и текущей датой
    order = Order(
        id=uuid4(),
        user_id=user_id,
        items=items,
        total_price=total_price,
        status=OrderStatus.PENDING,
        created_at=datetime.utcnow()
    )

    # Добавление и фиксация изменений в БД
    db.add(order)
    await db.commit()

    # Обновление объекта заказа из БД (например, если есть значения по умолчанию от сервера)
    await db.refresh(order)
    return order


async def get_order_by_id(db: AsyncSession, order_id: UUID) -> Optional[Order]:
    """
    Получает заказ по его UUID.
    """
    # Выполняем запрос к БД для поиска заказа по id
    result = await db.execute(select(Order).where(Order.id == order_id))
    return result.scalar_one_or_none()


async def update_order_status(db: AsyncSession, order_id: UUID, new_status: str) -> None:
    """
    Обновляет статус заказа. Бросает исключение, если заказ не найден.
    """
    # Создаём SQL выражение на обновление статуса по ID
    stmt = (
        update(Order)
        .where(Order.id == order_id)
        .values(status=new_status)
        .execution_options(synchronize_session="fetch")
    )

    # Выполняем обновление и проверяем, были ли затронуты строки
    result = await db.execute(stmt)
    if result.rowcount == 0:
        raise NoResultFound

    # Фиксируем изменения
    await db.commit()


async def get_orders_by_user_id(db: AsyncSession, user_id: int) -> List[Order]:
    """
    Возвращает список заказов, принадлежащих пользователю.
    """
    # Выполняем запрос для получения всех заказов пользователя
    result = await db.execute(select(Order).where(Order.user_id == user_id))
    return result.scalars().all()
