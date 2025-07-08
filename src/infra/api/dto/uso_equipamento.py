from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from src.domain.models.enums.status_de_uso import StatusUsoEquipamento

class CursoResponse(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True

class CargoResponse(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True

class EquipamentoResponse(BaseModel):
    codigo_tombamento: str
    codigo_tag: Optional[str] = None
    modelo: Optional[str] = None
    marca: Optional[str] = None
    cor: Optional[str] = None

    class Config:
        from_attributes = True

class FuncionarioResponse(BaseModel):
    id: int
    email: str
    nome: Optional[str] = None
    codigo_cartao: Optional[str] = None
    curso: Optional[CursoResponse] = None
    cargo: Optional[CargoResponse] = None

    class Config:
        from_attributes = True

class UsoEquipamentoResponse(BaseModel):
    protocolo: int
    data_aluguel: datetime
    data_devolucao: Optional[datetime] = None
    status: StatusUsoEquipamento
    equipamento: EquipamentoResponse
    funcionario: FuncionarioResponse

    class Config:
        from_attributes = True