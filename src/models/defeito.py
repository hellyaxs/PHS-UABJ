from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from src.config.database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class Defeito(Base):
    __tablename__ = "defeito"
    
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String(250))
    equipamento_codigo = Column(String(8), ForeignKey("equipamento.codigo"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relacionamentos
    equipamento = relationship("Equipamento", back_populates="defeitos")
    
    def __repr__(self):
        return f"Defeito(id={self.id}, equipamento_codigo={self.equipamento_codigo})"