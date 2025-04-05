from sqlalchemy import Column, Integer, String

from app.infrastructure.database.base import Base


class User(Base):
    """
    Модель таблицы пользователей.

    Атрибуты:
        id (int): Уникальный идентификатор пользователя.
        email (str): Email пользователя (уникальный).
        hashed_password (str): Хешированный пароль пользователя.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
