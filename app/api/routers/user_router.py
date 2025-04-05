from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Pydantic-схема для отображения информации о пользователе
from app.schemas.user import UserOut

# Зависимости для получения текущего пользователя и сессии БД
from app.api.deps import get_current_user, get_db

# SQLAlchemy-модель пользователя
from app.infrastructure.models.user import User

# Инициализация маршрутизатора
router = APIRouter()


@router.get("/me", response_model=UserOut, tags=["Users"])
async def get_me(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    """
    Возвращает данные текущего авторизованного пользователя.

    Параметры:
    - current_user: объект пользователя, полученный через зависимость get_current_user.
    - db: сессия асинхронной базы данных (не используется, но добавлена для консистентности).

    Возвращает:
    - Сериализованные данные пользователя (UserOut).
    """
    return current_user
