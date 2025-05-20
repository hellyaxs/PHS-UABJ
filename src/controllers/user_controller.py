from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.config.database.database import get_db
from src.models.user import User

user_router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@user_router.post("/")
def criar_usuario(email: str, username: str, password: str, full_name: str, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    novo_usuario = User(
        email=email,
        username=username,
        hashed_password=password,
        full_name=full_name
    )
    
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@user_router.get("/{user_id}")
def ler_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario = db.query(User).filter(User.id == user_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@user_router.put("/{user_id}")
def atualizar_usuario(user_id: int, email: str = None, full_name: str = None, db: Session = Depends(get_db)):
    usuario = db.query(User).filter(User.id == user_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if email:
        usuario.email = email
    if full_name:
        usuario.full_name = full_name
    
    db.commit()
    db.refresh(usuario)
    return usuario

@user_router.delete("/{user_id}")
def deletar_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario = db.query(User).filter(User.id == user_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    db.delete(usuario)
    db.commit()
    return {"message": "Usuário deletado com sucesso"}