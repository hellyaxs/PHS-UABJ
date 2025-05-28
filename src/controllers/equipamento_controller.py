from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.config.database.database import get_db
from src.models.equipamento import Equipamento
from src.schemas.equipamento import EquipamentoCreate

equipamento_router = APIRouter(
    prefix="/equipamentos",
    tags=["equipamentos"]
)

@equipamento_router.post("/", response_model=EquipamentoCreate)
def criar_equipamento(equipamento: EquipamentoCreate, db: Session = Depends(get_db)):
    if db.query(Equipamento).filter(Equipamento.codigo_tombamento == equipamento.codigo_tombamento).first():
        raise HTTPException(status_code=400, detail="Código de tombamento já cadastrado")
    
    novo_equipamento = Equipamento(
        codigo_tombamento=equipamento.codigo_tombamento,
        modelo=equipamento.modelo,
        marca=equipamento.marca,
        cor=equipamento.cor
    )
    
    db.add(novo_equipamento)
    db.commit()
    db.refresh(novo_equipamento)
    return novo_equipamento

@equipamento_router.get("/")
def listar_equipamentos(db: Session = Depends(get_db)):
    equipamentos = db.query(Equipamento).all()
    return equipamentos

@equipamento_router.get("/{codigo}")
def ler_equipamento(codigo: str, db: Session = Depends(get_db)):
    equipamento = db.query(Equipamento).filter(Equipamento.codigo == codigo).first()
    if equipamento is None:
        raise HTTPException(status_code=404, detail="Equipamento não encontrado")
    return equipamento

@equipamento_router.put("/{codigo}")
def atualizar_equipamento(codigo: str, nome: str = None, modelo: str = None, marca: str = None, cor: str = None, db: Session = Depends(get_db)):
    equipamento = db.query(Equipamento).filter(Equipamento.codigo == codigo).first()
    if equipamento is None:
        raise HTTPException(status_code=404, detail="Equipamento não encontrado")
    
    if nome:
        equipamento.nome = nome
    if modelo:
        equipamento.modelo = modelo
    if marca:
        equipamento.marca = marca
    if cor:
        equipamento.cor = cor
    
    db.commit()
    db.refresh(equipamento)
    return equipamento

@equipamento_router.delete("/{codigo_tombamento}")
def deletar_equipamento(codigo_tombamento: str, db: Session = Depends(get_db)):
    equipamento = db.query(Equipamento).filter(Equipamento.codigo_tombamento == codigo_tombamento).first()
    if equipamento is None:
        raise HTTPException(status_code=404, detail="Equipamento não encontrado")
    
    db.delete(equipamento)
    db.commit()
    return {"message": "Equipamento deletado com sucesso"}