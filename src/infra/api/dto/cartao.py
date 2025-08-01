from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class CartaoBase(BaseModel):
    rfid: str
    nivel_acesso: int
    status: str
    funcionario_id: Optional[int] = None
    ultima_entrada: datetime | None = None

class CartaoCreate(CartaoBase):
    pass

class CartaoUpdate(CartaoBase):
    rfid: str | None = None
    nivel_acesso: int | None = None
    status: str | None = None
    

class CartaoInDB(CartaoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 