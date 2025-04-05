from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

# Репозитории пользователей
from app.infrastructure.repositories.user_repository import get_user_by_email, create_user

# Сервисы аутентификации
from app.domain.services.auth.auth_service import (
    verify_password,
    create_access_token,
    create_refresh_token,
)

# Подключение к базе данных
from app.infrastructure.database.session import get_db

# Конфигурация приложения
from app.core.config import settings

# Pydantic-схемы
from app.schemas.user import UserCreate, UserOut
from app.schemas.token import Token

# Инициализация маршрутизатора
router = APIRouter()


@router.post("/register/", response_model=UserOut)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Регистрирует нового пользователя по email и паролю.
    """
    # Проверка: существует ли пользователь с таким email
    existing_user = await get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует",
        )

    # Создание нового пользователя
    new_user = await create_user(db, user_data.email, user_data.password)
    return new_user


@router.post("/token/", response_model=Token)
async def get_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Получение access и refresh токенов по схеме OAuth2 Password Flow.
    """
    # Получение пользователя по email (username)
    user = await get_user_by_email(db, form_data.username)

    # Проверка корректности пароля
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные"
        )

    # Генерация токенов
    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})

    # Возвращаем токены
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh/", response_model=Token)
async def refresh_token(refresh_token: str):
    """
    Обновление access токена с использованием refresh токена.
    """
    try:
        # Декодируем refresh токен
        payload = jwt.decode(
            refresh_token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

        # Извлекаем email из токена
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        # Генерируем новый access токен
        new_access_token = create_access_token(data={"sub": email})

        return {
            "access_token": new_access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    except JWTError:
        # Ошибка декодирования токена
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
