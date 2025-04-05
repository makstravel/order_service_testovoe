"""
Точка входа в приложение FastAPI — Order Management Service.

Функциональность:
- JWT-аутентификация (ранее Google OAuth 2.0)
- Заказы с кешированием в Redis
- Очереди сообщений через RabbitMQ
- Фоновая обработка через Celery
- CORS, Rate Limiting, Middleware
"""

import asyncio
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.domain.services.shared.rate_limiter import limiter
from app.api.routers.auth_router import router as auth_router
from app.api.routers.order_router import router as order_router
from app.api.routers.user_router import router as user_router
from app.domain.services.messaging.rabbitmq_consumer import start_consumer

app = FastAPI(
    title="Сервис заказов",
    version="1.0.0",
    description="Сервис управления заказами с использованием Redis, Celery и RabbitMQ",
)

# Запуск фонового задания при старте приложения (RabbitMQ consumer)
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_consumer())


# Настройка CORS: разрешённые источники (домены)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение middleware для сессий (если требуется хранение токенов)
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

# Подключение лимитера запросов
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Обработка превышения лимитов
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})


# Регистрация маршрутов
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(order_router, tags=["Orders"])
