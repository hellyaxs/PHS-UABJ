from pydantic import BaseModel
from datetime import datetime

class DefeitoBase(BaseModel):
    descricao: str
    equipamento_codigo: str

class DefeitoCreate(DefeitoBase):
    pass

class Defeito(DefeitoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 