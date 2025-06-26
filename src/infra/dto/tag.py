from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from src.domain.models.enums.status_de_uso import StatusTag

class TagResponse(BaseModel):
    id: int
    rfid: str
    nome: str
    ultima_leitura: Optional[datetime] = None
    nivel_acesso: int
    status: StatusTag
    equipamento_codigo: Optional[str] = None

    class Config:
        from_attributes = True

class TagCreate(BaseModel):
    rfid: str
    nome: str
    ultima_leitura: Optional[str] = None
    nivel_acesso: int
    status: str
    equipamento_codigo: Optional[str] = None

class TagUpdate(BaseModel):
    nome: Optional[str] = None
    nivel_acesso: Optional[int] = None
    status: Optional[StatusTag] = None
    equipamento_codigo: Optional[str] = None