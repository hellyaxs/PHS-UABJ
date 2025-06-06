"""create_defeito_table

Revision ID: 21bab657a8d6
Revises: 30bd71464394
Create Date: 2025-06-04 20:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision: str = '21bab657a8d6'
down_revision: Union[str, None] = '30bd71464394'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('defeito',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('descricao', sa.String(length=250), nullable=True),
        sa.Column('equipamento_codigo', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['equipamento_codigo'], ['equipamento.codigo_tombamento'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_defeito_id'), 'defeito', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_defeito_id'), table_name='defeito')
    op.drop_table('defeito')
