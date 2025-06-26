from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from src.infra.config.database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class Curso(Base):
    __tablename__ = "curso"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    
    # Adicionar o relacionamento bidirecional
    funcionarios = relationship("Funcionario", back_populates="curso")

