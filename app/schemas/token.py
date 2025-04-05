from pydantic import BaseModel

class Token(BaseModel):
    """
    Схема ответа, содержащая JWT access и refresh токены.
    """
    access_token: str
    refresh_token: str
    token_type: str
