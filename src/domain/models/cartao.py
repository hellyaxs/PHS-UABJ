from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from src.infra.config.database.database import Base

class Cartao(Base):
    __tablename__ = "cartao"
    
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome: str = Column(String(150), nullable=False)
    rfid: str = Column(String(50), nullable=False, unique=True)
    nivel_acesso: int = Column(Integer, nullable=False)
    status: str = Column(String(50), nullable=False)
    ultima_entrada: datetime = Column(DateTime, nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Cartao(id={self.id}, nome={self.nome}, rfid={self.rfid}, nivel_acesso={self.nivel_acesso}, status={self.status}, ultima_entrada={self.ultima_entrada}, created_at={self.created_at})>"