from pydantic import BaseModel

class FuncionarioBase(BaseModel):
    id: int
    email: str
    codigo_cartao: str
    nome: str
    curso_id: int
class FuncionarioCreate(FuncionarioBase):
    pass

class Funcionario(FuncionarioBase):
    class Config:
        from_attributes = True 