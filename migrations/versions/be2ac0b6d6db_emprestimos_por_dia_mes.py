"""emprestimos_por_dia_mes

Revision ID: be2ac0b6d6db
Revises: add_equipamento_codigo_to_tags
Create Date: 2025-07-15 16:45:08.879264

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be2ac0b6d6db'
down_revision: Union[str, None] = 'add_equipamento_codigo_to_tags'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    view_query_postgresql = """
    SELECT 
        EXTRACT(DAY FROM ue.data_aluguel) as dia_mes,
        COUNT(*) as total_emprestimos
    FROM uso_equipamento ue
    GROUP BY dia_mes
    ORDER BY dia_mes
    """

    view_query_mysql = """
    SELECT 
        DAY(ue.data_aluguel) as dia_mes,
        COUNT(*) as total_emprestimos
    FROM uso_equipamento ue
    GROUP BY dia_mes
    ORDER BY dia_mes
    """

    bind = op.get_bind()
    dialect_name = bind.dialect.name

    if dialect_name == 'postgresql':
        query = view_query_postgresql
    else:
        query = view_query_mysql

    op.execute(f"CREATE VIEW emprestimos_por_dia_mes AS {query}")


def downgrade() -> None:
    op.execute("DROP VIEW IF EXISTS emprestimos_por_dia_mes")
