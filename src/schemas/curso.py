from pydantic import BaseModel

class CursoBase(BaseModel):
    nome: str

class CursoCreate(CursoBase):
    pass

class Curso(CursoBase):
    id: int

    class Config:
        from_attributes = True 