from typing import Optional
from pydantic import BaseModel

class FuncionarioBase(BaseModel):
    id: Optional[int] = None
    email: str
    codigo_cartao: Optional[str]
    curso_id: int
    cargo_id: int
    nome: Optional[str] = None
class FuncionarioCreate(FuncionarioBase):
    pass

class Funcionario(FuncionarioBase):
    class Config:
        from_attributes = True 