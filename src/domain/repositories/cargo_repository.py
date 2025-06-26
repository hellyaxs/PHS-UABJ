from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.domain.models.cargo import Cargo
from src.infra.dto.cargo import CargoUpdate

class CargoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Cargo).all()
    
    def get_by_id(self, id: int):
        return self.db.query(Cargo).filter(Cargo.id == id).first()
    
    def create(self, cargo: Cargo):
        self.db.add(cargo)
        self.db.commit()
        self.db.refresh(cargo)
        return cargo
    
    def update(self, cargo_id: int, cargo_update: CargoUpdate) -> Cargo:
        db_cargo = self.db.query(Cargo).filter(Cargo.id == cargo_id).first()
        if db_cargo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cargo não encontrado"
            )
        
        update_data = cargo_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_cargo, field, value)
        
        self.db.commit()
        self.db.refresh(db_cargo)
        return db_cargo