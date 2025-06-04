from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from src.config.database.database import get_db
from src.models.equipamento import Equipamento
from src.models.funcionario import Funcionario
from src.models.curso import Curso
from src.models.cargo import Cargo
from src.models.usoequipamento import UsoEquipamento
from src.models.enums.status_de_uso import StatusUsoEquipamento
from pydantic import BaseModel
from datetime import datetime

locacao_router = APIRouter(
    prefix="/uso-equipamento",
    tags=["uso-equipamento"]
)

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
    codigo_tag: str
    modelo: Optional[str] = None
    marca: Optional[str] = None
    cor: Optional[str] = None

    class Config:
        from_attributes = True

class FuncionarioResponse(BaseModel):
    id: int
    email: str
    codigo_cartao: Optional[str] = None
    nome: str
    curso: Optional[CursoResponse] = None
    cargo: Optional[CargoResponse] = None

    class Config:
        from_attributes = True

class UsoEquipamentoResponse(BaseModel):
    protocolo: int
    equipamento_codigo: str
    data_aluguel: datetime
    data_devolucao: Optional[datetime] = None
    status: StatusUsoEquipamento
    equipamento: Optional[EquipamentoResponse] = None
    funcionario: Optional[FuncionarioResponse] = None

    class Config:
        from_attributes = True

@locacao_router.get("/", response_model=List[UsoEquipamentoResponse])
async def listar_usos_equipamento(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista todos os registros de uso de equipamento com seus relacionamentos.
    """
    usos = db.query(UsoEquipamento).offset(skip).limit(limit).all()
    return usos

@locacao_router.get("/{protocolo}", response_model=UsoEquipamentoResponse)
async def obter_uso_equipamento(
    protocolo: int,
    db: Session = Depends(get_db)
):
    """
    Obtém um registro específico de uso de equipamento pelo protocolo.
    """
    uso = db.query(UsoEquipamento).filter(UsoEquipamento.protocolo == protocolo).first()
    if not uso:
        raise HTTPException(status_code=404, detail="Registro de uso não encontrado")
    return uso

@locacao_router.get("/funcionario/{id}", response_model=List[UsoEquipamentoResponse])
async def listar_usos_por_funcionario(
    id: int,
    db: Session = Depends(get_db)
):
    """
    Lista todos os registros de uso de equipamento de um funcionário específico.
    """
    usos = db.query(UsoEquipamento).filter(UsoEquipamento.funcionario_id == id).all()
    return usos

@locacao_router.get("/equipamento/{codigo}", response_model=List[UsoEquipamentoResponse])
async def listar_usos_por_equipamento(
    codigo: str,
    db: Session = Depends(get_db)
):
    """
    Lista todos os registros de uso de um equipamento específico.
    """
    usos = db.query(UsoEquipamento).filter(UsoEquipamento.equipamento_codigo == codigo).all()
    return usos 