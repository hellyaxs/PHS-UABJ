from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from src.domain.repositories.uso_equipamento import UsoEquipamentoRepository
from src.infra.config.database.database import get_db
from src.infra.api.dto.uso_equipamento import UsoEquipamentoResponse, FuncionarioResponse
from src.domain.models.views.dia_mais_usado_view import DiaMaisUsadoViewResponse

locacao_router = APIRouter(
    prefix="/uso-equipamento",
    tags=["uso-equipamento"]
)


def get_uso_equipamento_repository(db: Session = Depends(get_db)) -> UsoEquipamentoRepository:
    return UsoEquipamentoRepository(db)

@locacao_router.get("/", response_model=List[UsoEquipamentoResponse])
def get_all_uso_equipamento(repo: UsoEquipamentoRepository = Depends(get_uso_equipamento_repository)):
    return repo.get_all()

@locacao_router.get("/pendentes", response_model=List[FuncionarioResponse])
async def listar_usos_pendentes(
    repo: UsoEquipamentoRepository = Depends(get_uso_equipamento_repository)
):
    funcionarios, _ = repo.get_equipamentos_pendentes()
    return funcionarios

@locacao_router.get("/emprestimos-por-dia", response_model=List[DiaMaisUsadoViewResponse])
async def listar_emprestimos_por_dia(
    repo: UsoEquipamentoRepository = Depends(get_uso_equipamento_repository)
):
    return repo.get_emprestimos_por_dia()

@locacao_router.get("/{protocolo}", response_model=UsoEquipamentoResponse)
async def obter_uso_equipamento(
    protocolo: int,
    repo: UsoEquipamentoRepository = Depends(get_uso_equipamento_repository)
):
    return repo.get_by_protocolo(protocolo)

@locacao_router.get("/funcionario/{id}", response_model=List[UsoEquipamentoResponse])
async def listar_usos_por_funcionario(
    id: int,
    repo: UsoEquipamentoRepository = Depends(get_uso_equipamento_repository)
):
    return repo.get_by_funcionario_id(id)

@locacao_router.get("/equipamento/{codigo}", response_model=List[UsoEquipamentoResponse])
async def listar_usos_por_equipamento(
    codigo: str,
    repo: UsoEquipamentoRepository = Depends(get_uso_equipamento_repository)
):
    return repo.get_by_equipamento_codigo(codigo)

