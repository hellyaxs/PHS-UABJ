from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.domain.repositories.cartao_repository import CartaoRepository
from src.infra.config.database.database import get_db
from src.domain.models.cartao import Cartao
from src.domain.models.funcionario import Funcionario
from src.infra.dto.cartao import CartaoCreate, CartaoUpdate, CartaoInDB

router_cartao = APIRouter(
    prefix="/cartoes",
    tags=["cartoes"],
    responses={404: {"description": "Cartão não encontrado"}},
)

@router_cartao.post("/", response_model=CartaoInDB, status_code=status.HTTP_201_CREATED)
def create_cartao(cartao: CartaoCreate, db: Session = Depends(get_db)):
    return CartaoRepository(db).create_cartao(cartao)

@router_cartao.get("/nao_associados", response_model=List[CartaoInDB])
def read_cartoes_nao_associados(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return CartaoRepository(db).get_cartoes_nao_associados(skip, limit)

@router_cartao.get("/", response_model=List[CartaoInDB])
def read_cartoes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return CartaoRepository(db).get_all(skip, limit)

@router_cartao.get("/{cartao_id}", response_model=CartaoInDB)
def read_cartao(cartao_id: int, db: Session = Depends(get_db)):
    return CartaoRepository(db).get_by_id(cartao_id)

@router_cartao.get("/rfid/{rfid}", response_model=CartaoInDB)
def read_cartao_by_rfid(rfid: str, db: Session = Depends(get_db)):
    return CartaoRepository(db).get_by_rfid(rfid)

@router_cartao.put("/{cartao_id}", response_model=CartaoInDB)
def update_cartao(cartao_id: int, cartao: CartaoUpdate, db: Session = Depends(get_db)):
    return CartaoRepository(db).update(cartao_id, cartao)

@router_cartao.delete("/{cartao_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cartao(cartao_id: int, db: Session = Depends(get_db)):
    return CartaoRepository(db).delete(cartao_id)