from datetime import datetime
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from src.domain.models.equipamento import Equipamento
from src.domain.models.tags import Tag
from src.infra.config.database.database import get_db
from src.infra.api.dto.tag import TagCreate
from src.domain.models.enums.status_de_uso import StatusTag

class TagRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all(self):
        return self.db.query(Tag).all()
    
    def get_by_id(self, tag_id: int):
        """
        Obtém uma tag específica pelo ID.
        """
        tag = self.db.query(Tag).filter(Tag.id == tag_id).first()
        if not tag:
            raise HTTPException(status_code=404, detail="Tag não encontrada")
        return tag

    def create(self, tag: TagCreate):
        try:
            if self.db.query(Tag).filter(Tag.rfid == tag.rfid).first():
                raise HTTPException(status_code=400, detail="Tag já existe no sistema")
            db_tag = Tag(
                rfid=tag.rfid,
                nome=tag.nome,
                nivel_acesso=tag.nivel_acesso,
                equipamento_codigo=tag.equipamento_codigo,
                ultima_leitura=datetime.now(),
                status=StatusTag(tag.status)
            )
            self.db.add(db_tag)
            self.db.commit()
            if tag.equipamento_codigo:
                equipamento = self.db.query(Equipamento).filter(Equipamento.codigo_tombamento == tag.equipamento_codigo).first()
                if equipamento:
                    equipamento.codigo_tag = tag.rfid
                    self.db.commit()
                    self.db.refresh(equipamento)
            self.db.refresh(db_tag)
            return db_tag
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str("Erro ao criar tag"))
    
    def update(self, tag_id: int, tag: Tag):
        """
        Atualiza uma tag existente.
        """
        db_tag = self.db.query(Tag).filter(Tag.id == tag_id).first()
        if not db_tag:
            raise HTTPException(status_code=404, detail="Tag não encontrada")
        
        update_data = tag.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_tag, key, value)
        
        self.db.commit()
        self.db.refresh(db_tag)
        return db_tag
    
    def delete(self, tag_id: int):
        """
        Remove uma tag.
        """
        db_tag = self.db.query(Tag).filter(Tag.id == tag_id).first()
        if not db_tag:
            raise HTTPException(status_code=404, detail="Tag não encontrada")
        
        self.db.delete(db_tag)
        self.db.commit()
        return {"message": "Tag removida com sucesso"} 
    
    def toggle_status(self, tag_rfid: str, status: bool):
        """
        Alterna o status de uma tag.
        """
        db_tag = self.db.query(Tag).filter(Tag.rfid == tag_rfid).first()
        if not db_tag:
            raise HTTPException(status_code=404, detail="Tag não encontrada")
        db_tag.status = StatusTag.ATIVO if status else StatusTag.INATIVO
        self.db.commit()
        return db_tag