from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Схема для создания нового пользователя (регистрация)"""
    email: EmailStr
    password: str


class UserOut(BaseModel):
    """Схема для возврата информации о пользователе (без пароля)"""
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
