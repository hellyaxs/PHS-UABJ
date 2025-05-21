from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from src.config.database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
class Funcionario(Base):
    __tablename__ = "funcionario"
    
    cpf = Column(String(11), primary_key=True, index=True)
    codigo_cartao = Column(String(10))
    nome = Column(String(150), nullable=False)
    curso_id = Column(Integer, ForeignKey("curso.id"), nullable=False)
    
    # Relacionamentos
    curso = relationship("Curso", back_populates="funcionarios")
    usos_equipamentos = relationship("UsoEquipamento", back_populates="funcionario")
    
    def __repr__(self):
        return f"Funcionario(cpf={self.cpf}, nome={self.nome})"
