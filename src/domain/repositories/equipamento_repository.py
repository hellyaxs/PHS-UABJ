from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from src.domain.models.equipamento import Equipamento
from src.domain.models.tags import Tag
from src.infra.config.database.database import get_db
from src.infra.dto.equipamento import EquipamentoCreate

class EquipamentoRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all(self):
        return self.db.query(Equipamento).options(    
        joinedload(Equipamento.defeito)
    ).all() 

    def get_by_id(self, codigo: str):
        equipamento = self.db.query(Equipamento).options(    
            joinedload(Equipamento.defeito)
        ).filter(Equipamento.codigo_tombamento == codigo).first()
        if equipamento is None:
                raise HTTPException(status_code=404, detail="Equipamento não encontrado")
        return equipamento

    def create(self, equipamento: EquipamentoCreate) -> Equipamento:
        if self.db.query(Equipamento).filter(Equipamento.codigo_tombamento == equipamento.codigo_tombamento).first():
            raise HTTPException(status_code=400, detail="Código de tombamento já cadastrado")
        
        novo_equipamento = Equipamento(
            codigo_tombamento=equipamento.codigo_tombamento,
            modelo=equipamento.modelo,
            marca=equipamento.marca,
            cor=equipamento.cor
        )
        
        self.db.add(novo_equipamento)
        self.db.commit()
        self.db.refresh(novo_equipamento)
        return novo_equipamento
    
    def update(self, codigo: str, nome: str = None, modelo: str = None, marca: str = None, cor: str = None) -> Equipamento:
        equipamento = self.db.query(Equipamento).filter(Equipamento.codigo == codigo).first()
        if equipamento is None:
            raise HTTPException(status_code=404, detail="Equipamento não encontrado")
        
        if nome:
            equipamento.nome = nome
        if modelo:
            equipamento.modelo = modelo
        if marca:
            equipamento.marca = marca
        if cor:
            equipamento.cor = cor
        
        self.db.commit()
        self.db.refresh(equipamento)
        return equipamento
    
    def delete(self, codigo_tombamento: str) -> Equipamento:
        equipamento = self.db.query(Equipamento).filter(Equipamento.codigo_tombamento == codigo_tombamento).first()
        if equipamento is None:
            raise HTTPException(status_code=404, detail="Equipamento não encontrado")
        
        self.db.delete(equipamento)
        self.db.commit()
        return {"message": "Equipamento deletado com sucesso"}
    
    def get_equipamentos_nao_associados(self) -> list[Equipamento]:
        """
        Retorna a lista de equipamentos que não estão associados a uma tag.
        """
        # Subquery para encontrar os códigos de tombamento que estão em uso
        equipamentos_associados = select(Tag.equipamento_codigo).where(Tag.equipamento_codigo != None).subquery()
        
        # Query principal para encontrar equipamentos não associados
        equipamentos = self.db.query(Equipamento).filter(~Equipamento.codigo_tombamento.in_(equipamentos_associados)).all()
        return equipamentos