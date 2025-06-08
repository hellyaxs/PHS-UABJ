from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.config.database.database import get_db
from src.models.cartao import Cartao
from src.models.funcionario import Funcionario
from src.schemas.cartao import CartaoCreate, CartaoUpdate, CartaoInDB

router_cartao = APIRouter(
    prefix="/cartoes",
    tags=["cartoes"],
    responses={404: {"description": "Cartão não encontrado"}},
)

@router_cartao.post("/", response_model=CartaoInDB, status_code=status.HTTP_201_CREATED)
def create_cartao(cartao: CartaoCreate, db: Session = Depends(get_db)):
    """
    Cria um novo cartão.
    """
    db_cartao = Cartao(**cartao.model_dump())
    db.add(db_cartao)
    db.commit()
    db.refresh(db_cartao)
    return db_cartao

@router_cartao.get("/nao_associados", response_model=List[CartaoInDB])
def read_cartoes_nao_associados(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retorna a lista de cartões não associados a funcionários.
    """
    # Subquery para encontrar os códigos de cartão que estão em uso
    cartoes_em_uso = db.query(Funcionario.codigo_cartao).filter(Funcionario.codigo_cartao != None).subquery()
    
    # Query principal para encontrar cartões não associados
    cartoes = db.query(Cartao).filter(~Cartao.rfid.in_(cartoes_em_uso)).offset(skip).limit(limit).all()
    return cartoes

@router_cartao.get("/", response_model=List[CartaoInDB])
def read_cartoes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retorna a lista de cartões não associados a funcionários.
    """
    
    # Query principal para encontrar cartões não associados
    cartoes = db.query(Cartao).offset(skip).limit(limit).all()
    return cartoes

@router_cartao.get("/{cartao_id}", response_model=CartaoInDB)
def read_cartao(cartao_id: int, db: Session = Depends(get_db)):
    """
    Retorna um cartão específico pelo ID.
    """
    db_cartao = db.query(Cartao).filter(Cartao.id == cartao_id).first()
    if db_cartao is None:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
    return db_cartao

@router_cartao.get("/rfid/{rfid}", response_model=CartaoInDB)
def read_cartao_by_rfid(rfid: str, db: Session = Depends(get_db)):
    """
    Retorna um cartão específico pelo RFID.
    """
    db_cartao = db.query(Cartao).filter(Cartao.rfid == rfid).first()
    if db_cartao is None:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
    return db_cartao

@router_cartao.put("/{cartao_id}", response_model=CartaoInDB)
def update_cartao(cartao_id: int, cartao: CartaoUpdate, db: Session = Depends(get_db)):
    """
    Atualiza um cartão existente.
    """
    db_cartao = db.query(Cartao).filter(Cartao.id == cartao_id).first()
    if db_cartao is None:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
    
    update_data = cartao.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_cartao, key, value)
    
    db.commit()
    db.refresh(db_cartao)
    return db_cartao

@router_cartao.delete("/{cartao_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cartao(cartao_id: int, db: Session = Depends(get_db)):
    """
    Remove um cartão.
    """
    db_cartao = db.query(Cartao).filter(Cartao.id == cartao_id).first()
    if db_cartao is None:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
    
    db.delete(db_cartao)
    db.commit()
    return None 