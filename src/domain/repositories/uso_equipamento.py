from datetime import datetime, timedelta
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from src.domain.models.enums.status_de_uso import StatusUsoEquipamento
from src.domain.models.funcionario import Funcionario
from src.domain.models.usoequipamento import UsoEquipamento
from src.domain.models.views.dia_mais_usado_view import EmprestimosPorDiaView
from src.infra.api.dto.uso_equipamento import UsoEquipamentoResponse

class UsoEquipamentoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, uso_equipamento: UsoEquipamento):
        self.db.add(uso_equipamento)
        self.db.commit()
        self.db.refresh(uso_equipamento)
        return uso_equipamento
    
    def get_all(self, skip: int = 0, limit: int = 100):
        query = self.db.query(UsoEquipamento).options(
        joinedload(UsoEquipamento.equipamento),
        joinedload(UsoEquipamento.funcionario).joinedload(Funcionario.curso),
        joinedload(UsoEquipamento.funcionario).joinedload(Funcionario.cargo)
        )

        total = query.count()
        resultados = query.offset(skip).limit(limit).all() 

        return resultados, total
 

    def get_by_id(self, id: int):
        return self.db.query(UsoEquipamento).filter(UsoEquipamento.id == id).first()
    
    def get_by_protocolo(self, protocolo: int) -> UsoEquipamentoResponse:
        """
        Obtém um registro específico de uso de equipamento pelo protocolo.
        """
        uso = self.db.query(UsoEquipamento).filter(UsoEquipamento.protocolo == protocolo).first()
        if not uso:
            raise HTTPException(status_code=404, detail="Registro de uso não encontrado")
        return uso
    
    def get_by_funcionario_id(self, funcionario_id: int) -> List[UsoEquipamentoResponse]:
        return self.db.query(UsoEquipamento).filter(UsoEquipamento.funcionario_id == funcionario_id).all()
    
    def get_equipamentos_pendentes(self):
        """
        Lista todos os registros de uso de equipamento pendentes.
        """
        usos = self.db.query(UsoEquipamento).options(
            joinedload(UsoEquipamento.funcionario),
            joinedload(UsoEquipamento.equipamento)
        ).filter(UsoEquipamento.data_devolucao == None).all()
        funcionarios = []
        for uso in usos:
            if uso.data_aluguel + timedelta(hours=8) < datetime.now():
                funcionarios.append(uso.funcionario_id)
                # self.db.query(UsoEquipamento).filter(UsoEquipamento.protocolo == uso.protocolo).update({"status": StatusUsoEquipamento.PENDENTE})
                self.db.commit()
                self.db.refresh(uso)
                
        funcionarios = self.db.query(Funcionario).filter(Funcionario.id.in_(funcionarios)).all()
        return funcionarios, usos
    
    def get_emprestimos_por_dia(self):
        return self.db.query(EmprestimosPorDiaView).all()
    
    def get_by_equipamento_codigo(self, codigo: str) -> List[UsoEquipamentoResponse]:
        return self.db.query(UsoEquipamento).filter(UsoEquipamento.equipamento_codigo == codigo).all()
    
    def update_uso_equipamento(self, uso_equipamento: UsoEquipamento):
        self.db.add(uso_equipamento)
        self.db.commit()
        self.db.refresh(uso_equipamento)
        return uso_equipamento