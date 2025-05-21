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
    if db.query(Equipamento).filter(Equipamento.codigo == equipamento.codigo).first():
        raise HTTPException(status_code=400, detail="Código de equipamento já cadastrado")
    
    novo_equipamento = Equipamento(
        codigo=equipamento.codigo,
        nome=equipamento.nome,
        modelo=equipamento.modelo,
        marca=equipamento.marca,
        cor=equipamento.cor
    )
    
    db.add(novo_equipamento)
    db.commit()
    db.refresh(novo_equipamento)
    return novo_equipamento

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

@equipamento_router.delete("/{codigo}")
def deletar_equipamento(codigo: str, db: Session = Depends(get_db)):
    equipamento = db.query(Equipamento).filter(Equipamento.codigo == codigo).first()
    if equipamento is None:
        raise HTTPException(status_code=404, detail="Equipamento não encontrado")
    
    db.delete(equipamento)
    db.commit()
    return {"message": "Equipamento deletado com sucesso"} 