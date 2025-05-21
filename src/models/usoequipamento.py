from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from src.config.database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class UsoEquipamento(Base):
    __tablename__ = "uso_equipamento"
    
    protocolo = Column(Integer, primary_key=True, index=True)
    equipamento_codigo = Column(String(8), ForeignKey("equipamento.codigo"), nullable=False)
    funcionario_cpf = Column(String(11), ForeignKey("funcionario.cpf"), nullable=False)
    data_aluguel = Column(DateTime, nullable=False, default=datetime.now())
    data_devolucao = Column(DateTime, nullable=True)
    
    # Relacionamentos
    equipamento = relationship("Equipamento", back_populates="usos")
    funcionario = relationship("Funcionario", back_populates="usos_equipamentos")
    
    def __repr__(self):
        return f"UsoEquipamento(protocolo={self.protocolo}, data_aluguel={self.data_aluguel})"