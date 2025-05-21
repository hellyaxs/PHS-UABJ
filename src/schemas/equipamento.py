from pydantic import BaseModel

class EquipamentoBase(BaseModel):
    codigo: str
    nome: str
    modelo: str
    marca: str
    cor: str

class EquipamentoCreate(EquipamentoBase):
    pass

class Equipamento(EquipamentoBase):
    class Config:
        from_attributes = True 