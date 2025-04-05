from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# Инициализация контекста для хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет соответствие открытого пароля и хэша.

    :param plain_password: Пароль в открытом виде
    :param hashed_password: Захэшированный пароль из БД
    :return: True, если пароли совпадают, иначе False
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Хэширует пароль для хранения в базе данных.

    :param password: Открытый пароль
    :return: Хэш пароля
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Создаёт JWT access токен с заданными данными и временем жизни.

    :param data: Данные для кодирования (например, {"sub": email})
    :param expires_delta: Время жизни токена. По умолчанию берётся из конфигурации.
    :return: JWT access token в виде строки
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
