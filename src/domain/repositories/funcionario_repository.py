from fastapi import Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from src.domain.models.curso import Curso
from src.domain.models.usoequipamento import UsoEquipamento
from src.infra.config.database.database import get_db
from src.domain.models.funcionario import Funcionario
from src.infra.dto.funcionario import FuncionarioCreate

class FuncionarioRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all(self) -> list[Funcionario]:
        return self.db.query(Funcionario).all()
    
    def get_by_id(self, id: int) -> Funcionario:
        return self.db.query(Funcionario).filter(Funcionario.id == id).first()
    
    def get_by_cpf(self, cpf: str) -> Funcionario:
        funcionario = self.db.query(Funcionario).filter(Funcionario.cpf == cpf).first()
        if funcionario is None:
            raise HTTPException(status_code=404, detail="Funcionário não encontrado")
        return funcionario
    
    def get_by_email(self, email: str):
        return self.db.query(Funcionario).filter(Funcionario.email == email).first()
    
    def get_by_course_id(self, course_id: int) -> list[Funcionario]:
        # Verifica se o curso existe
        curso = self.db.query(Curso).filter(Curso.id == course_id).first()
        if not curso:
            raise HTTPException(status_code=404, detail="Curso não encontrado")
        
        funcionarios = self.db.query(Funcionario).filter(Funcionario.curso_id == course_id).all()
        return funcionarios

    def funcionario_mais_uso(self):
        """
        Retorna o nome do funcionário que mais usou equipamentos.
        """
        # Query para contar usos por funcionário e pegar o com mais usos
        funcionario_mais_uso = self.db.query(
            Funcionario.nome,
            func.count(UsoEquipamento.protocolo).label('total_usos')
        ).join(UsoEquipamento, Funcionario.id == UsoEquipamento.funcionario_id)\
        .group_by(Funcionario.id, Funcionario.nome)\
        .order_by(func.count(UsoEquipamento.protocolo).desc())\
        .first()
        
        if funcionario_mais_uso is None:
            raise HTTPException(status_code=404, detail="Nenhum funcionário encontrado")
        
        return {
            "nome": funcionario_mais_uso.nome,
            "total_usos": funcionario_mais_uso.total_usos
        } 
    
    def create(self, funcionario: Funcionario) -> Funcionario:
        # Verifica se o CPF já está cadastrado
        if self.db.query(Funcionario).filter(Funcionario.email == funcionario.email).first():
            raise HTTPException(status_code=400, detail="email já cadastrado")
        
        curso = self.db.query(Curso).filter(Curso.id == funcionario.curso_id).first()
        if not curso:
            raise HTTPException(status_code=404, detail="Curso não encontrado")
        
        novo_funcionario = Funcionario(
            email=funcionario.email,
            codigo_cartao=funcionario.codigo_cartao if funcionario.codigo_cartao else None,
            curso_id=funcionario.curso_id,
            cargo_id=funcionario.cargo_id,
            nome=funcionario.nome,
        )
        
        self.db.add(novo_funcionario)
        self.db.commit()
        self.db.refresh(novo_funcionario)
        return novo_funcionario
    

    def update(self, cpf: str, funcionario: FuncionarioCreate) -> Funcionario:
        funcionario_existente = self.db.query(Funcionario).filter(Funcionario.cpf == cpf).first()
        if funcionario_existente is None:
            raise HTTPException(status_code=404, detail="Funcionário não encontrado")
        
        # Verifica se o curso existe
        curso = self.db.query(Curso).filter(Curso.id == funcionario.curso_id).first()
        if not curso:
            raise HTTPException(status_code=404, detail="Curso não encontrado")
        
        funcionario_existente.codigo_cartao = funcionario.codigo_cartao
        funcionario_existente.nome = funcionario.nome
        funcionario_existente.curso_id = funcionario.curso_id
        
        self.db.commit()
        self.db.refresh(funcionario_existente)
        return funcionario_existente

    def get_funcionarios_nao_associados(self):
        """
        Retorna a lista de funcionários que não estão associados a um cartão.
        """
        funcionarios = self.db.query(Funcionario).filter(Funcionario.codigo_cartao == None).all()
        return funcionarios
    
    def delete(self, cpf: str):
        funcionario = self.db.query(Funcionario).filter(Funcionario.cpf == cpf).first()
        if funcionario is None:
            raise HTTPException(status_code=404, detail="Funcionário não encontrado")
        
        self.db.delete(funcionario)
        self.db.commit()
        return {"message": "Funcionário deletado com sucesso"}