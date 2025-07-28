"""create_uso_equipamento_table

Revision ID: 6b679c10d0fe
Revises: 98ec0f811ee9
Create Date: 2025-06-04 19:45:12.334 UTC

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6b679c10d0fe'
down_revision: Union[str, None] = '98ec0f811ee9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # Criar a tabela uso_equipamento
    op.create_table('uso_equipamento',
        sa.Column('protocolo', sa.Integer(), nullable=False),
        sa.Column('equipamento_codigo', sa.String(length=50), nullable=False),
        sa.Column('funcionario_id', sa.Integer(), nullable=False),
        sa.Column('data_aluguel', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('data_devolucao', sa.DateTime(), nullable=True),
        sa.Column('status', postgresql.ENUM('ALOCADO', 'DEVOLVIDO', 'EM_USO', 'PENDENTE', 'EMAIL_ENVIADO','DEVOLVIDO_DEFEITO', name='statususoequipamento'), nullable=False, server_default='ALOCADO'),
        sa.ForeignKeyConstraint(['equipamento_codigo'], ['equipamento.codigo_tombamento'], ),
        sa.ForeignKeyConstraint(['funcionario_id'], ['funcionario.id'], ),
        sa.PrimaryKeyConstraint('protocolo')
    )
    op.create_index(op.f('ix_uso_equipamento_protocolo'), 'uso_equipamento', ['protocolo'], unique=False)


def downgrade() -> None:
    # Remover a tabela uso_equipamento
    op.drop_index(op.f('ix_uso_equipamento_protocolo'), table_name='uso_equipamento')
    op.drop_table('uso_equipamento')
    
    # Remover o enum StatusUsoEquipamento
    status_uso_equipamento = postgresql.ENUM(name='statususoequipamento')
    status_uso_equipamento.drop(op.get_bind())
