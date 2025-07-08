from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from src.domain.repositories.equipamento_repository import EquipamentoRepository
from src.infra.config.database.database import get_db
from src.domain.models.equipamento import Equipamento
from src.infra.api.dto.equipamento import EquipamentoCreate
from src.domain.models.tags import Tag

equipamento_router = APIRouter(
    prefix="/equipamentos",
    tags=["equipamentos"]
)

@equipamento_router.post("/", response_model=EquipamentoCreate)
def criar_equipamento(equipamento: EquipamentoCreate, db: Session = Depends(get_db)):
    return EquipamentoRepository(db).create(equipamento)

@equipamento_router.get("/nao_associados")
def listar_equipamentos_nao_associados(db: Session = Depends(get_db)):
    return EquipamentoRepository(db).get_equipamentos_nao_associados()

@equipamento_router.get("/")
def listar_equipamentos(db: Session = Depends(get_db)):
    return EquipamentoRepository(db).get_all()

@equipamento_router.get("/{codigo}")
def ler_equipamento(codigo: str, db: Session = Depends(get_db)):
    return EquipamentoRepository(db).get_by_id(codigo)

@equipamento_router.put("/{codigo}")
def atualizar_equipamento(codigo: str, nome: str = None, modelo: str = None, marca: str = None, cor: str = None, db: Session = Depends(get_db)):
    return EquipamentoRepository(db).update(codigo, nome, modelo, marca, cor)

@equipamento_router.delete("/{codigo_tombamento}")
async def deletar_equipamento(codigo_tombamento: str, db: Session = Depends(get_db)):
    return EquipamentoRepository(db).delete(codigo_tombamento)