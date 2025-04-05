
from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# Контекст для хэширования и проверки паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict) -> str:
    """
    Создаёт access-токен с заданными данными и сроком действия из конфигурации.

    :param data: Словарь с данными для токена (например, {"sub": email})
    :return: JWT access token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def create_refresh_token(data: dict) -> str:
    """
    Создаёт refresh-токен с заданными данными и сроком действия из конфигурации.

    :param data: Словарь с данными для токена
    :return: JWT refresh token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет, соответствует ли открытый пароль хэшу.

    :param plain_password: Пароль в открытом виде
    :param hashed_password: Хэш пароля из БД
    :return: True, если пароли совпадают, иначе False
    """
    return pwd_context.verify(plain_password, hashed_password)
