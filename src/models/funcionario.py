from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from src.config.database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class Funcionario(Base):
    __tablename__ = "funcionario"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(50), primary_key=True, index=True)
    codigo_cartao = Column(String(10))
    curso_id = Column(Integer, ForeignKey("curso.id"), nullable=False)
    cargo_id = Column(Integer, ForeignKey("cargo.id"), nullable=False)
    
    # Relacionamentos
    curso = relationship("Curso", back_populates="funcionarios")
    cargo = relationship("Cargo", back_populates="funcionarios")
    usos_equipamentos = relationship("UsoEquipamento", back_populates="funcionario")
    
    def __repr__(self):
        return f"Funcionario(cpf={self.email}, nome={self.nome})"
