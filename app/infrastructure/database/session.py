from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from app.core.config import settings

# Формирование строки подключения к PostgreSQL (используется asyncpg)
DATABASE_URL = (
    f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}"
    f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
)

# Инициализация асинхронного движка SQLAlchemy
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Вывод SQL-запросов в лог для отладки
    future=True
)

# Асинхронная фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False  # Не инвалидировать объекты после коммита
)


async def get_db() -> AsyncSession:
    """
    Возвращает асинхронную сессию к базе данных.

    Используется как зависимость FastAPI через Depends.
    Закрывает сессию автоматически после завершения запроса.
    """
    async with AsyncSessionLocal() as session:
        yield session
