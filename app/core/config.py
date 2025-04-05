import os
from typing import List
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field

# Загружаем переменные окружения из .env файла, если он существует
dotenv_path = os.path.join(os.path.dirname(__file__), "../../.env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Settings(BaseSettings):
    """
    Основной класс конфигурации приложения.
    Все параметры читаются из переменных окружения с помощью Pydantic.
    """

    # Настройки PostgreSQL
    db_host: str = Field(..., env="DB_HOST")
    db_port: int = Field(..., env="DB_PORT")
    db_name: str = Field(..., env="DB_NAME")
    db_user: str = Field(..., env="DB_USER")
    db_password: str = Field(..., env="DB_PASSWORD")

    # Настройки Redis
    redis_host: str = Field(..., env="REDIS_HOST")
    redis_port: int = Field(..., env="REDIS_PORT")
    cache_ttl_seconds: int = Field(300, env="CACHE_TTL_SECONDS")  # TTL кеша в секундах

    # Настройки RabbitMQ
    rabbitmq_host: str = Field(..., env="RABBITMQ_HOST")
    rabbitmq_port: int = Field(..., env="RABBITMQ_PORT")
    rabbitmq_user: str = Field(..., env="RABBITMQ_USER")
    rabbitmq_password: str = Field(..., env="RABBITMQ_PASSWORD")

    # Настройки безопасности
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(..., env="ALGORITHM")
    access_token_expire_minutes: int = Field(..., env="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(15, env="REFRESH_TOKEN_EXPIRE_DAYS")

    # Rate limiting
    rate_limit: str = Field(..., env="RATE_LIMIT")

    # CORS (origins)
    allowed_origins_raw: str = Field(..., env="ALLOWED_ORIGINS_RAW")

    @property
    def allowed_origins(self) -> List[str]:
        """
        Преобразует строку с CORS-оригинами в список строк.
        """
        return [x.strip() for x in self.allowed_origins_raw.split(",") if x.strip()]

    @property
    def database_url(self) -> str:
        """
        Формирует URL подключения к базе данных в формате для SQLAlchemy.
        """
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Экземпляр конфигурации, используется по всему проекту
settings = Settings()
