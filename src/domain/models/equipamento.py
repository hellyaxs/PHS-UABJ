from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from src.infra.config.database.database import Base
from sqlalchemy.orm import relationship

class Equipamento(Base):
    __tablename__ = "equipamento"
    
    codigo_tombamento = Column(String(50), primary_key=True, index=True) 
    codigo_tag = Column(String(10), default="")  
    modelo = Column(String(100))
    marca = Column(String(100))
    cor = Column(String(30))
    
    # Relacionamentos
    tag = relationship("Tag", back_populates="equipamento")
    usos = relationship("UsoEquipamento", back_populates="equipamento")
    defeitos = relationship("Defeito", back_populates="equipamento")
    
    def __repr__(self):
        return f"Equipamento(codigo_tombamento={self.codigo_tombamento}, modelo={self.modelo})"
    