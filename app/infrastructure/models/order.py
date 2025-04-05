from datetime import datetime
from uuid import uuid4


from sqlalchemy import Column, ForeignKey, JSON, Float, Enum as SqlEnum, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.infrastructure.database.base import Base
from app.domain.enums.order_status import OrderStatus


class Order(Base):
    """
    Модель таблицы заказов.

    Атрибуты:
        id (UUID): Уникальный идентификатор заказа.
        user_id (int): Идентификатор пользователя, сделавшего заказ.
        items (JSON): Список заказанных товаров в формате JSON.
        total_price (float): Общая стоимость заказа.
        status (OrderStatus): Статус текущего заказа.
        created_at (datetime): Дата и время создания заказа.
    """
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(ForeignKey("users.id"), nullable=False)

    items = Column(JSON, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(SqlEnum(OrderStatus, name="order_status"), default=OrderStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
