from slowapi import Limiter
from slowapi.util import get_remote_address

#  Инициализация rate limiter по IP-адресу
limiter = Limiter(
    key_func=get_remote_address
)
"""
Limiter используется для ограничения частоты запросов
на уровне FastAPI middleware. Настройки лимита можно задавать
на уровне маршрутов через декоратор @limiter.limit("100/minute")
"""
