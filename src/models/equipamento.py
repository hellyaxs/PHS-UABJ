from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from src.config.database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class Equipamento(Base):
    __tablename__ = "equipamento"
    
    codigo = Column(String(8), primary_key=True, index=True)
    nome = Column(String(100))
    modelo = Column(String(100))
    marca = Column(String(100))
    cor = Column(String(30))
    
    # Relacionamentos
    usos = relationship("UsoEquipamento", back_populates="equipamento")
    defeitos = relationship("Defeito", back_populates="equipamento")
    
    def __repr__(self):
        return f"Equipamento(codigo={self.codigo}, nome={self.nome})"
