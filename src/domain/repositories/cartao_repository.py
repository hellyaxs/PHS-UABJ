from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from src.domain.models.cartao import Cartao
from src.domain.models.funcionario import Funcionario
from src.infra.config.database.database import get_db
from src.infra.api.dto.cartao import CartaoCreate

class CartaoRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_cartao(self, cartao: CartaoCreate):
        """
        Cria um novo cartão.
        """
        # Filtra os dados para remover campos que não existem no modelo Cartao
        cartao_data = cartao.model_dump()
        funcionario_id = cartao_data.pop('funcionario_id', None)  # Remove funcionario_id dos dados
        if self.db.query(Cartao).filter(Cartao.rfid == cartao.rfid).first():
            raise HTTPException(status_code=400, detail="Cartão já existe no sistema")
        db_cartao = Cartao(**cartao_data)

        self.db.add(db_cartao)
        self.db.commit()
        self.db.refresh(db_cartao)
        
        if funcionario_id:
            funcionario = self.db.query(Funcionario).filter(Funcionario.id == funcionario_id).first()
            if funcionario:
                funcionario.codigo_cartao = cartao.rfid
                self.db.commit()
                self.db.refresh(funcionario)
        
        return db_cartao
    
    def get_all(self, skip: int = 0, limit: int = 100) -> list[Cartao]:
        """
        Retorna a lista de cartões não associados a funcionários.
        """
        # Query principal para encontrar cartões não associados
        cartoes = self.db.query(Cartao).offset(skip).limit(limit).all()
        return cartoes
    
    def get_by_id(self, cartao_id: int) -> Cartao:
        """
        Retorna um cartão específico pelo ID.
        """
        db_cartao = self.db.query(Cartao).filter(Cartao.id == cartao_id).first()
        if db_cartao is None:
            raise HTTPException(status_code=404, detail="Cartão não encontrado")
        return db_cartao
    
    def get_by_rfid(self, rfid: str) -> Cartao:
        """
        Retorna um cartão específico pelo RFID.
        """
        db_cartao = self.db.query(Cartao).filter(Cartao.rfid == rfid).first()
        if db_cartao is None:
            raise HTTPException(status_code=404, detail="Cartão não encontrado")
        return db_cartao
    
    def update(self, cartao_id: int, cartao: Cartao) -> Cartao:
        """
        Atualiza um cartão existente.
        """
        db_cartao = self.db.query(Cartao).filter(Cartao.id == cartao_id).first()
        if db_cartao is None:
            raise HTTPException(status_code=404, detail="Cartão não encontrado")
        
        update_data = cartao.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_cartao, key, value)
        
        self.db.commit()
        self.db.refresh(db_cartao)
        return db_cartao
    
    def delete(self, id: int) -> Cartao:
        """
        Remove um cartão.
        """
        db_cartao = self.db.query(Cartao).filter(Cartao.id == id).first()
        if db_cartao is None:
            raise HTTPException(status_code=404, detail="Cartão não encontrado")
        
        self.db.delete(db_cartao)
        self.db.commit()
        return None 
    def get_cartoes_nao_associados(self, skip: int = 0, limit: int = 100) -> list[Cartao]:
        """
        Retorna a lista de cartões não associados a funcionários.
        """
        # Subquery para encontrar os códigos de cartão que estão em uso
        cartoes_em_uso = self.db.query(Funcionario.codigo_cartao).filter(Funcionario.codigo_cartao != None).subquery()
        
        # Query principal para encontrar cartões não associados
        cartoes = self.db.query(Cartao).filter(~Cartao.rfid.in_(cartoes_em_uso)).offset(skip).limit(limit).all()
        return cartoes