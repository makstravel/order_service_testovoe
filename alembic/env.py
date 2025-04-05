import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

# Добавляем корень проекта в PYTHONPATH
sys.path.append(os.path.abspath(os.getcwd()))

from app.core.config import settings
from app.infrastructure.database.base import Base

# Настройка логирования Alembic
config = context.config
fileConfig(config.config_file_name)

# Используем синхронный URL для Alembic
config.set_main_option("sqlalchemy.url", settings.database_url.replace("+asyncpg", ""))
target_metadata = Base.metadata


def run_migrations_offline():
    """Генерация SQL без подключения к БД"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Подключение к БД и применение миграций"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
