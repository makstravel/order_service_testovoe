from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.infrastructure.models.user import User
from passlib.context import CryptContext
from typing import Optional

# Контекст для хеширования паролей (используется bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Получение пользователя по email
async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """
    Ищет пользователя в базе данных по email.
    Возвращает объект User или None.
    """
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()

# Создание пользователя с хешированным паролем
async def create_user(db: AsyncSession, email: str, password: str) -> User:
    """
    Создает нового пользователя с хешированным паролем.
    """
    hashed_password = pwd_context.hash(password)
    user = User(email=email, hashed_password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
