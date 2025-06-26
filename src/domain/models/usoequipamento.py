from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from src.infra.config.database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from .enums.status_de_uso import StatusUsoEquipamento

class UsoEquipamento(Base):
    __tablename__ = "uso_equipamento"
    
    protocolo = Column(Integer, primary_key=True, index=True)
    equipamento_codigo = Column(String(50), ForeignKey("equipamento.codigo_tombamento"), nullable=False)
    funcionario_id = Column(Integer, ForeignKey("funcionario.id"), nullable=False)
    data_aluguel = Column(DateTime, nullable=False, default=datetime.now())
    data_devolucao = Column(DateTime, nullable=True)
    status = Column(SQLEnum(StatusUsoEquipamento), nullable=False, default=StatusUsoEquipamento.ALOCADO)
    
    # Relacionamentos
    equipamento = relationship("Equipamento", back_populates="usos")
    funcionario = relationship("Funcionario", back_populates="usos_equipamentos")
    
    def __repr__(self):
        return f"UsoEquipamento(protocolo={self.protocolo}, data_aluguel={self.data_aluguel})"