from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from src.domain.repositories.tag_repository import TagRepository
from src.infra.config.database.database import get_db
from src.infra.api.dto.tag import TagResponse, TagCreate, TagUpdate

tag_router = APIRouter(
    prefix="/tags",
    tags=["tags"]
)

@tag_router.get("/", response_model=List[TagResponse])
def get_all_tags(db: Session = Depends(get_db)):
    return TagRepository(db).get_all()

@tag_router.get("/{tag_id}", response_model=TagResponse)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    return TagRepository(db).get_by_id(tag_id)

@tag_router.post("/", response_model=TagResponse)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    return TagRepository(db).create(tag)

@tag_router.put("/{tag_id}", response_model=TagResponse)
def update_tag(tag_id: int, tag: TagUpdate, db: Session = Depends(get_db)):
    return TagRepository(db).update(tag_id, tag)

@tag_router.delete("/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    return TagRepository(db).delete(tag_id)