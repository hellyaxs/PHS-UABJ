from pydantic import BaseModel
from sqlalchemy import Column, Integer

from src.infra.config.database.database import Base

class EmprestimosPorDiaMesResponse(BaseModel):
    dia_mes: int
    total_emprestimos: int

class EmprestimosPorDiaMes(Base):
    __tablename__ = 'emprestimos_por_dia_mes'
    
    dia_mes = Column(Integer, primary_key=True)
    total_emprestimos = Column(Integer)