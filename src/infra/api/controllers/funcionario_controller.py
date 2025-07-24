from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.domain.repositories.funcionario_repository import FuncionarioRepository
from src.infra.config.database.database import get_db
from src.infra.api.dto.funcionario import FuncionarioCreate, Funcionario as FuncionarioSchema

funcionario_router = APIRouter(
    prefix="/funcionarios",
    tags=["funcionarios"], 
)

@funcionario_router.get("/mais_uso")
def funcionario_mais_uso(db: Session = Depends(get_db)):
    return FuncionarioRepository(db).funcionario_mais_uso()

@funcionario_router.post("/", response_model=FuncionarioSchema)
def criar_funcionario(funcionario: FuncionarioCreate, db: Session = Depends(get_db)):
    return FuncionarioRepository(db).create(funcionario)

@funcionario_router.get("/nao_associados",response_model=list[FuncionarioSchema])
def listar_funcionarios_nao_associados(db: Session = Depends(get_db)):
    return FuncionarioRepository(db).get_funcionarios_nao_associados()

@funcionario_router.get("/", response_model=list[FuncionarioSchema])
def listar_funcionarios(db: Session = Depends(get_db)):
    return FuncionarioRepository(db).get_all()

@funcionario_router.get("/{cpf}", response_model=FuncionarioSchema)
def ler_funcionario(cpf: str, db: Session = Depends(get_db)):
    return FuncionarioRepository(db).get_by_cpf(cpf)

@funcionario_router.get("/curso/{curso_id}", response_model=list[FuncionarioSchema])
def listar_funcionarios_curso(curso_id: int, db: Session = Depends(get_db)):
    return FuncionarioRepository(db).get_by_course_id(curso_id)

@funcionario_router.put("/{cpf}", response_model=FuncionarioSchema)
def atualizar_funcionario(cpf: str, funcionario: FuncionarioCreate, db: Session = Depends(get_db)):
    return FuncionarioRepository(db).update(cpf, funcionario)

@funcionario_router.delete("/{email}")
def deletar_funcionario(email: str, db: Session = Depends(get_db)):
    return FuncionarioRepository(db).delete(email)


