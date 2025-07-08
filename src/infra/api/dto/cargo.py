from pydantic import BaseModel, Field
from typing import Optional

class CargoBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100, description="Nome do cargo")
    descricao: Optional[str] = Field(None, max_length=255, description="Descrição detalhada do cargo")

class CargoCreate(CargoBase):
    pass

class CargoUpdate(CargoBase):
    nome: Optional[str] = Field(None, min_length=2, max_length=100, description="Nome do cargo")

class CargoResponse(CargoBase):
    id: int
    
    class Config:
        from_attributes = True