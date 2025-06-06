"""create_view_dia_mais_usado

Revision ID: a4b32f0ce908
Revises: 6b679c10d0fe
Create Date: 2025-06-04 15:33:43.010776

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4b32f0ce908'
down_revision: Union[str, None] = '6b679c10d0fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Query para PostgreSQL
    view_query_postgresql = """
    SELECT 
        EXTRACT(DOW FROM data_aluguel) as dia_semana_num,
        CASE EXTRACT(DOW FROM data_aluguel)
            WHEN 0 THEN 'Domingo'
            WHEN 1 THEN 'Segunda'
            WHEN 2 THEN 'Terça'
            WHEN 3 THEN 'Quarta'
            WHEN 4 THEN 'Quinta'
            WHEN 5 THEN 'Sexta'
            WHEN 6 THEN 'Sábado'
        END as dia_semana,
        CASE EXTRACT(DOW FROM data_aluguel)
            WHEN 0 THEN 'Dom'
            WHEN 1 THEN 'Seg'
            WHEN 2 THEN 'Ter'
            WHEN 3 THEN 'Qua'
            WHEN 4 THEN 'Qui'
            WHEN 5 THEN 'Sex'
            WHEN 6 THEN 'Sáb'
        END as dia_semana_abrev,
        COUNT(*) as total_emprestimos,
        COUNT(CASE WHEN status = 'ALOCADO' THEN 1 END) as emprestimos_ativos,
        COUNT(CASE WHEN status = 'DEVOLVIDO' THEN 1 END) as emprestimos_devolvidos,
        DATE(data_aluguel) as data_referencia
    FROM uso_equipamento
    GROUP BY 
        EXTRACT(DOW FROM data_aluguel),
        DATE(data_aluguel)
    ORDER BY dia_semana_num
    """
    
    # Query para MySQL/SQLite (sintaxe diferente)
    view_query_mysql = """
    SELECT 
        DAYOFWEEK(data_aluguel) as dia_semana_num,
        CASE DAYOFWEEK(data_aluguel)
            WHEN 1 THEN 'Domingo'
            WHEN 2 THEN 'Segunda'
            WHEN 3 THEN 'Terça'
            WHEN 4 THEN 'Quarta'
            WHEN 5 THEN 'Quinta'
            WHEN 6 THEN 'Sexta'
            WHEN 7 THEN 'Sábado'
        END as dia_semana,
        CASE DAYOFWEEK(data_aluguel)
            WHEN 1 THEN 'Dom'
            WHEN 2 THEN 'Seg'
            WHEN 3 THEN 'Ter'
            WHEN 4 THEN 'Qua'
            WHEN 5 THEN 'Qui'
            WHEN 6 THEN 'Sex'
            WHEN 7 THEN 'Sáb'
        END as dia_semana_abrev,
        COUNT(*) as total_emprestimos,
        COUNT(CASE WHEN status = 'ALOCADO' THEN 1 END) as emprestimos_ativos,
        COUNT(CASE WHEN status = 'DEVOLVIDO' THEN 1 END) as emprestimos_devolvidos,
        DATE(data_aluguel) as data_referencia
    FROM uso_equipamento
    GROUP BY 
        DAYOFWEEK(data_aluguel),
        DATE(data_aluguel)
    ORDER BY dia_semana_num
    """
    
    # Detectar o tipo de banco e usar a query apropriada
    bind = op.get_bind()
    dialect_name = bind.dialect.name
    
    if dialect_name == 'postgresql':
        query = view_query_postgresql
    else:  # MySQL, SQLite, etc.
        query = view_query_mysql
    
    # Criar a view
    op.execute(f"CREATE VIEW emprestimos_por_dia AS {query}")

def downgrade():
    op.execute("DROP VIEW IF EXISTS emprestimos_por_dia")

