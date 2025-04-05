from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

# Pydantic-схемы заказов
from app.schemas.order import OrderCreate, OrderOut, OrderUpdateStatus

# Модель пользователя для авторизации
from app.infrastructure.models.user import User

# Зависимости (получение БД и текущего пользователя)
from app.api.deps import get_db, get_current_user

# Сервисный слой для работы с заказами
from app.domain.services.order.order_service import (
    handle_order_creation,
    get_order_with_cache,
    update_order_status_service,
    get_user_orders_service,
)

# Инициализация маршрутизатора
router = APIRouter()


@router.post("/orders/", response_model=OrderOut)
async def create_order_api(
    order_data: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Создание нового заказа от имени текущего авторизованного пользователя.
    """
    # Вызов сервисного слоя для создания заказа
    order = await handle_order_creation(
        db=db,
        user_id=current_user.id,
        items=order_data.items,
        total_price=order_data.total_price
    )
    return order


@router.get("/orders/{order_id}/", response_model=OrderOut)
async def get_order(
    order_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Получение заказа по UUID. Сначала выполняется попытка получения из Redis-кеша,
    при отсутствии — данные извлекаются из базы данных.
    """
    order = await get_order_with_cache(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order


@router.patch("/orders/{order_id}/")
async def update_order_status_api(
    order_id: UUID,
    data: OrderUpdateStatus,
    db: AsyncSession = Depends(get_db)
):
    """
    Обновление статуса заказа. Владельцем может быть любой пользователь (доп. проверка не проводится).
    """
    await update_order_status_service(db, order_id, data.status)
    return {"message": "Статус заказа обновлён"}


@router.get("/orders/user/{user_id}/", response_model=List[OrderOut])
async def get_user_orders(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Получение списка заказов по ID пользователя. Доступ разрешён только владельцу.
    """
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Нет доступа к чужим заказам")

    return await get_user_orders_service(db, user_id)
