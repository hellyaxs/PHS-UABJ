from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from src.infra.config.database.database import get_db
from src.domain.models.funcionario import Funcionario
from src.domain.models.usoequipamento import UsoEquipamento
from src.domain.models.enums.status_de_uso import StatusUsoEquipamento
from datetime import datetime, timedelta
from src.infra.dto.uso_equipamento import UsoEquipamentoResponse, FuncionarioResponse
from src.domain.models.views.dia_mais_usado_view import DiaMaisUsadoViewResponse, EmprestimosPorDiaView

locacao_router = APIRouter(
    prefix="/uso-equipamento",
    tags=["uso-equipamento"]
)

@locacao_router.get("/", response_model=List[UsoEquipamentoResponse])
def get_all_uso_equipamento(db: Session = Depends(get_db)):
    uso_equipamentos = db.query(UsoEquipamento).options(
        joinedload(UsoEquipamento.equipamento),
        joinedload(UsoEquipamento.funcionario).joinedload(Funcionario.curso),
        joinedload(UsoEquipamento.funcionario).joinedload(Funcionario.cargo)
    ).all()
    
    return uso_equipamentos

@locacao_router.get("/pendentes", response_model=List[FuncionarioResponse])
async def listar_usos_pendentes(
    db: Session = Depends(get_db)
):
    """
    Lista todos os registros de uso de equipamento pendentes.
    """
    usos = db.query(UsoEquipamento).filter(UsoEquipamento.data_devolucao == None).all()
    funcionarios = []
    for uso in usos:
        if uso.data_aluguel + timedelta(hours=8) < datetime.now():
            funcionarios.append(uso.funcionario_id)
            db.query(UsoEquipamento).filter(UsoEquipamento.protocolo == uso.protocolo).update({"status": StatusUsoEquipamento.PENDENTE})
            db.commit()
            db.refresh(uso)
            
    funcionarios = db.query(Funcionario).filter(Funcionario.id.in_(funcionarios)).all()
    return funcionarios

@locacao_router.get("/emprestimos-por-dia", response_model=List[DiaMaisUsadoViewResponse])
async def listar_emprestimos_por_dia(
    db: Session = Depends(get_db)
):
    """
    Lista todos os registros de uso de equipamento por dia.
    """
    usos = db.query(EmprestimosPorDiaView).all()
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

