from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.infra.config.database.database import get_db
from src.domain.models.tags import Tag
from src.domain.models.enums.status_de_uso import StatusTag
from src.infra.dto.tag import TagResponse, TagCreate, TagUpdate
from datetime import datetime

tag_router = APIRouter(
    prefix="/tags",
    tags=["tags"]
)


@tag_router.get("/", response_model=List[TagResponse])
def get_all_tags(db: Session = Depends(get_db)):
    """
    Lista todas as tags cadastradas.
    """
    return db.query(Tag).all()

@tag_router.get("/{tag_id}", response_model=TagResponse)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    """
    Obtém uma tag específica pelo ID.
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag não encontrada")
    return tag

@tag_router.post("/", response_model=TagResponse)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    """
    Cria uma nova tag.
    """
    db_tag = Tag(
        rfid=tag.rfid,
        nome=tag.nome,
        nivel_acesso=tag.nivel_acesso,
        equipamento_codigo=tag.equipamento_codigo,
        ultima_leitura=datetime.now(),
        status=StatusTag(tag.status)
    )
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

@tag_router.put("/{tag_id}", response_model=TagResponse)
def update_tag(tag_id: int, tag: TagUpdate, db: Session = Depends(get_db)):
    """
    Atualiza uma tag existente.
    """
    db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag não encontrada")
    
    update_data = tag.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_tag, key, value)
    
    db.commit()
    db.refresh(db_tag)
    return db_tag

@tag_router.delete("/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    """
    Remove uma tag.
    """
    db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag não encontrada")
    
    db.delete(db_tag)
    db.commit()
    return {"message": "Tag removida com sucesso"} 