from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.infra.config.database.database import get_db
from src.infra.config.security.jwt import get_current_user
from src.domain.models.curso import Curso
from src.infra.dto.curso import CursoCreate, Curso as CursoSchema

curso_router = APIRouter(
    prefix="/cursos",
    tags=["cursos"],
)

@curso_router.post("/", response_model=CursoSchema)
def criar_curso(curso: CursoCreate, db: Session = Depends(get_db)):
    # Verifica se já existe um curso com o mesmo nome
    if db.query(Curso).filter(Curso.nome == curso.nome).first():
        raise HTTPException(status_code=400, detail="Já existe um curso com este nome")
    
    novo_curso = Curso(
        nome=curso.nome
    )
    
    db.add(novo_curso)
    db.commit()
    db.refresh(novo_curso)
    return novo_curso

@curso_router.get("/", response_model=list[CursoSchema])
def listar_cursos(db: Session = Depends(get_db)):
    cursos = db.query(Curso).all()
    return cursos

@curso_router.get("/{curso_id}", response_model=CursoSchema)
def ler_curso(curso_id: int, db: Session = Depends(get_db)):
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    return curso

@curso_router.put("/{curso_id}", response_model=CursoSchema)
def atualizar_curso(curso_id: int, curso: CursoCreate, db: Session = Depends(get_db)):
    curso_existente = db.query(Curso).filter(Curso.id == curso_id).first()
    if curso_existente is None:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    
    # Verifica se o novo nome já existe em outro curso
    curso_com_mesmo_nome = db.query(Curso).filter(Curso.nome == curso.nome, Curso.id != curso_id).first()
    if curso_com_mesmo_nome:
        raise HTTPException(status_code=400, detail="Já existe um curso com este nome")
    
    curso_existente.nome = curso.nome
    db.commit()
    db.refresh(curso_existente)
    return curso_existente

@curso_router.delete("/{curso_id}")
def deletar_curso(curso_id: int, db: Session = Depends(get_db)):
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    
    db.delete(curso)
    db.commit()
    return {"message": "Curso deletado com sucesso"} 