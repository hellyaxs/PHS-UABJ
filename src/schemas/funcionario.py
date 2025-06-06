from pydantic import BaseModel

class FuncionarioBase(BaseModel):
    email: str
    codigo_cartao: str
    curso_id: int
    cargo_id: int
class FuncionarioCreate(FuncionarioBase):
    pass

class Funcionario(FuncionarioBase):
    class Config:
        from_attributes = True 