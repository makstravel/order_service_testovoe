from enum import Enum

class OrderStatus(str, Enum):
    """
    Перечисление возможных статусов заказа.
    """
    PENDING = "PENDING"
    PAID = "PAID"
    SHIPPED = "SHIPPED"
    CANCELED = "CANCELED"
