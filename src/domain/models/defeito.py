from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from src.infra.config.database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class Defeito(Base):
    __tablename__ = "defeito"
    
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String(250))
    equipamento_codigo = Column(String(50), ForeignKey("equipamento.codigo_tombamento"), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relacionamentos
    equipamento = relationship("Equipamento", back_populates="defeito")
    
    def __repr__(self):
        return f"Defeito(id={self.id}, equipamento_codigo={self.equipamento_codigo})"