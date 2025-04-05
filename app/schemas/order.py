from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import List, Dict

from app.domain.enums.order_status import OrderStatus


class OrderCreate(BaseModel):
    """
    Схема запроса для создания нового заказа.
    """
    items: List[Dict[str, str]]
    total_price: float


class OrderOut(BaseModel):
    """
    Схема ответа, представляющая заказ.
    """
    id: UUID
    user_id: int
    items: List[Dict[str, str]]
    total_price: float
    status: OrderStatus

    model_config = ConfigDict(from_attributes=True)  # Позволяет использовать ORM-объекты


class OrderUpdateStatus(BaseModel):
    """
    Схема запроса для обновления статуса заказа.
    """
    status: OrderStatus
