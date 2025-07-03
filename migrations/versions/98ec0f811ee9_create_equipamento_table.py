"""create_equipamento_table

Revision ID: 98ec0f811ee9
Revises: 2a39b4318a28
Create Date: 2025-06-04 19:58:55.334 UTC

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '98ec0f811ee9'
down_revision: Union[str, None] = '2a39b4318a28'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('equipamento',
        sa.Column('codigo_tombamento', sa.String(length=50), nullable=False),
        sa.Column('codigo_tag', sa.String(length=100), nullable=True, server_default=''),
        sa.Column('modelo', sa.String(length=100), nullable=True),
        sa.Column('marca', sa.String(length=100), nullable=True),
        sa.Column('cor', sa.String(length=30), nullable=True),
        sa.PrimaryKeyConstraint('codigo_tombamento'),
    )
    op.create_index(op.f('ix_equipamento_codigo_tombamento'), 'equipamento', ['codigo_tombamento'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_equipamento_codigo_tombamento'), table_name='equipamento')
    op.drop_table('equipamento')
