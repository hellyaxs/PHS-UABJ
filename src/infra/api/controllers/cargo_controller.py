from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.domain.repositories.cargo_repository import CargoRepository
from src.infra.config.database.database import get_db
from src.domain.models.cargo import Cargo
from src.infra.api.dto.cargo import CargoCreate, CargoResponse, CargoUpdate

router_cargo = APIRouter(
    prefix="/cargos",
    tags=["cargos"], 

)

@router_cargo.post("/", response_model=CargoResponse, status_code=status.HTTP_201_CREATED)
def create_cargo(cargo: CargoCreate, db: Session = Depends(get_db)):
    db_cargo = Cargo(**cargo.model_dump())
    db.add(db_cargo)
    db.commit()
    db.refresh(db_cargo)
    return db_cargo

@router_cargo.get("/", response_model=List[CargoResponse])
def list_cargos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cargos = db.query(Cargo).offset(skip).limit(limit).all()
    return cargos

@router_cargo.get("/{cargo_id}", response_model=CargoResponse)
def get_cargo(cargo_id: int, db: Session = Depends(get_db)):
    cargo = db.query(Cargo).filter(Cargo.id == cargo_id).first()
    if cargo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cargo não encontrado"
        )
    return cargo

@router_cargo.put("/{cargo_id}", response_model=CargoResponse)
def update_cargo(cargo_id: int, cargo_update: CargoUpdate, db: Session = Depends(get_db)):
    return CargoRepository(db).update(cargo_id, cargo_update)

@router_cargo.delete("/{cargo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cargo(cargo_id: int, db: Session = Depends(get_db)):
    db_cargo = db.query(Cargo).filter(Cargo.id == cargo_id).first()
    if db_cargo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cargo não encontrado"
        )
    
    db.delete(db_cargo)
    db.commit()
    return None