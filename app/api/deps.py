from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

# Конфигурация приложения
from app.core.config import settings

# Репозиторий пользователя
from app.infrastructure.repositories.user_repository import get_user_by_email

# Сессия подключения к БД
from app.infrastructure.database.session import get_db

# Инициализация схемы OAuth2 с использованием эндпоинта получения токена
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
):
    """
    Получает текущего пользователя на основе переданного JWT токена.

    Шаги:
    1. Извлекает и декодирует токен.
    2. Валидирует его подпись.
    3. Извлекает email из поля `sub`.
    4. Получает пользователя по email из БД.

    Если токен недействителен или пользователь не найден — вызывается HTTP 401.

    :param token: JWT-токен из заголовка авторизации.
    :param db: Асинхронная сессия базы данных.
    :return: Объект пользователя.
    """
    # Исключение для невалидных токенов
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Невозможно проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Декодирование токена
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

        # Извлечение email из payload
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Получение пользователя из БД
    user = await get_user_by_email(db, email)
    if user is None:
        raise credentials_exception

    return user
