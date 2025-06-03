from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.config.database.database import get_db
from src.config.jwt import get_current_user
from src.models.funcionario import Funcionario
from src.models.curso import Curso
from src.schemas.funcionario import FuncionarioCreate, Funcionario as FuncionarioSchema

funcionario_router = APIRouter(
    prefix="/funcionarios",
    tags=["funcionarios"], 
    dependencies=[Depends(get_current_user)]
)

@funcionario_router.post("/", response_model=FuncionarioSchema)
def criar_funcionario(funcionario: FuncionarioCreate, db: Session = Depends(get_db)):
    # Verifica se o CPF já está cadastrado
    if db.query(Funcionario).filter(Funcionario.cpf == funcionario.cpf).first():
        raise HTTPException(status_code=400, detail="CPF já cadastrado")
    
    # Verifica se o curso existe
    curso = db.query(Curso).filter(Curso.id == funcionario.curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    
    novo_funcionario = Funcionario(
        cpf=funcionario.cpf,
        codigo_cartao=funcionario.codigo_cartao,
        nome=funcionario.nome,
        curso_id=funcionario.curso_id
    )
    
    db.add(novo_funcionario)
    db.commit()
    db.refresh(novo_funcionario)
    return novo_funcionario

@funcionario_router.get("/", response_model=list[FuncionarioSchema])
def listar_funcionarios(db: Session = Depends(get_db)):
    funcionarios = db.query(Funcionario).all()
    return funcionarios

@funcionario_router.get("/{cpf}", response_model=FuncionarioSchema)
def ler_funcionario(cpf: str, db: Session = Depends(get_db)):
    funcionario = db.query(Funcionario).filter(Funcionario.cpf == cpf).first()
    if funcionario is None:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return funcionario

@funcionario_router.get("/curso/{curso_id}", response_model=list[FuncionarioSchema])
def listar_funcionarios_curso(curso_id: int, db: Session = Depends(get_db)):
    # Verifica se o curso existe
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    
    funcionarios = db.query(Funcionario).filter(Funcionario.curso_id == curso_id).all()
    return funcionarios

@funcionario_router.put("/{cpf}", response_model=FuncionarioSchema)
def atualizar_funcionario(cpf: str, funcionario: FuncionarioCreate, db: Session = Depends(get_db)):
    funcionario_existente = db.query(Funcionario).filter(Funcionario.cpf == cpf).first()
    if funcionario_existente is None:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    
    # Verifica se o curso existe
    curso = db.query(Curso).filter(Curso.id == funcionario.curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    
    funcionario_existente.codigo_cartao = funcionario.codigo_cartao
    funcionario_existente.nome = funcionario.nome
    funcionario_existente.curso_id = funcionario.curso_id
    
    db.commit()
    db.refresh(funcionario_existente)
    return funcionario_existente

@funcionario_router.delete("/{cpf}")
def deletar_funcionario(cpf: str, db: Session = Depends(get_db)):
    funcionario = db.query(Funcionario).filter(Funcionario.cpf == cpf).first()
    if funcionario is None:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    
    db.delete(funcionario)
    db.commit()
    return {"message": "Funcionário deletado com sucesso"} 