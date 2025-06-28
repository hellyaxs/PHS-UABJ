from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.infra.config.database.database import get_db
from src.domain.models.defeito import Defeito
from src.domain.models.equipamento import Equipamento
from src.infra.dto.defeito import DefeitoCreate, Defeito as DefeitoSchema

defeito_router = APIRouter(
    prefix="/defeitos",
    tags=["defeitos"]
)

@defeito_router.post("/", response_model=DefeitoSchema)
def criar_defeito(defeito: DefeitoCreate, db: Session = Depends(get_db)):
    # Verifica se o equipamento existe
    equipamento = db.query(Equipamento).filter(Equipamento.codigo_tombamento == defeito.equipamento_codigo).first()
    if not equipamento:
        raise HTTPException(status_code=404, detail="Equipamento não encontrado")
    
    novo_defeito = Defeito(
        descricao=defeito.descricao,
        equipamento_codigo=defeito.equipamento_codigo
    )
    
    db.add(novo_defeito)
    db.commit()
    db.refresh(novo_defeito)
    return novo_defeito

@defeito_router.get("/{defeito_id}", response_model=DefeitoSchema)
def ler_defeito(defeito_id: int, db: Session = Depends(get_db)):
    defeito = db.query(Defeito).filter(Defeito.id == defeito_id).first()
    if defeito is None:
        raise HTTPException(status_code=404, detail="Defeito não encontrado")
    return defeito

@defeito_router.get("/equipamento/{equipamento_codigo}", response_model=list[DefeitoSchema])
def listar_defeitos_equipamento(equipamento_codigo: str, db: Session = Depends(get_db)):
    # Verifica se o equipamento existe
    equipamento = db.query(Equipamento).filter(Equipamento.codigo_tombamento == equipamento_codigo).first()
    if not equipamento:
        raise HTTPException(status_code=404, detail="Equipamento não encontrado")
    
    defeitos = db.query(Defeito).filter(Defeito.equipamento_codigo == equipamento_codigo).all()
    return defeitos

@defeito_router.put("/{defeito_id}", response_model=DefeitoSchema)
def atualizar_defeito(defeito_id: int, defeito: DefeitoCreate, db: Session = Depends(get_db)):
    defeito_existente = db.query(Defeito).filter(Defeito.id == defeito_id).first()
    if defeito_existente is None:
        raise HTTPException(status_code=404, detail="Defeito não encontrado")
    
    if defeito.equipamento_codigo:
        # Verifica se o novo equipamento existe
        equipamento = db.query(Equipamento).filter(Equipamento.codigo_tombamento == defeito.equipamento_codigo).first()
        if not equipamento:
            raise HTTPException(status_code=404, detail="Equipamento não encontrado")
        defeito_existente.equipamento_codigo = defeito.equipamento_codigo
    
    if defeito.descricao:
        defeito_existente.descricao = defeito.descricao
    
    db.commit()
    db.refresh(defeito_existente)
    return defeito_existente

@defeito_router.delete("/{defeito_id}")
def deletar_defeito(defeito_id: int, db: Session = Depends(get_db)):
    defeito = db.query(Defeito).filter(Defeito.id == defeito_id).first()
    if defeito is None:
        raise HTTPException(status_code=404, detail="Defeito não encontrado")
    
    db.delete(defeito)
    db.commit()
    return {"message": "Defeito deletado com sucesso"} 