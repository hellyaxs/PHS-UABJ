from sqlalchemy import Column, Integer, String, Date, DateTime
from src.config.database.database import Base
from pydantic import BaseModel
from datetime import datetime


class DiaMaisUsadoViewResponse(BaseModel):
    dia_semana_num: int
    data_referencia: datetime
    dia_semana: str
    dia_semana_abrev: str
    total_emprestimos: int
    emprestimos_ativos: int
    emprestimos_devolvidos: int


class EmprestimosPorDiaView(Base):
    __tablename__ = 'emprestimos_por_dia'
    
    # Chave primária composta para evitar problemas
    dia_semana_num = Column(Integer, primary_key=True)
    data_referencia = Column(Date, primary_key=True)
    
    dia_semana = Column(String(10))
    dia_semana_abrev = Column(String(3))
    total_emprestimos = Column(Integer)
    emprestimos_ativos = Column(Integer)
    emprestimos_devolvidos = Column(Integer)