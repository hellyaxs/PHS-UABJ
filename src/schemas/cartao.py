from datetime import datetime
from pydantic import BaseModel

class CartaoBase(BaseModel):
    nome: str
    rfid: str
    nivel_acesso: int
    status: str
    ultima_entrada: datetime | None = None

class CartaoCreate(CartaoBase):
    pass

class CartaoUpdate(CartaoBase):
    nome: str | None = None
    rfid: str | None = None
    nivel_acesso: int | None = None
    status: str | None = None

class CartaoInDB(CartaoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 