from sqlalchemy import Column, DateTime, Integer, String, Enum as SQLEnum, ForeignKey
from src.infra.config.database.database import Base
from src.domain.models.enums.status_de_uso import StatusTag
from sqlalchemy.orm import relationship

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rfid = Column(String, unique=True, index=True)
    nome = Column(String, index=True)
    ultima_leitura = Column(DateTime)
    nivel_acesso = Column(Integer)
    status = Column(SQLEnum(StatusTag), nullable=False, default=StatusTag.ATIVO)
    equipamento_codigo = Column(String(50), ForeignKey("equipamento.codigo_tombamento"), nullable=True)
    
    # Relacionamento com Equipamento
    equipamento = relationship("Equipamento", back_populates="tag")
