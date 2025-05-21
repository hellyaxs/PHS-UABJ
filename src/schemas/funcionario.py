from pydantic import BaseModel

class FuncionarioBase(BaseModel):
    cpf: str
    codigo_cartao: str
    nome: str
    curso_id: int

class FuncionarioCreate(FuncionarioBase):
    pass

class Funcionario(FuncionarioBase):
    class Config:
        from_attributes = True 