from sqlalchemy import Column, Integer, String
from src.config.database.database import Base
from sqlalchemy.orm import relationship

class Cargo(Base):
    __tablename__ = "cargo"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    
    funcionarios = relationship("Funcionario", back_populates="cargo")
    
    def __repr__(self):
        return f"Cargo(id={self.id}, nome={self.nome})"