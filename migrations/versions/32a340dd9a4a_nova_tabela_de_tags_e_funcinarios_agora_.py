"""nova tabela de tags e funcinarios agora tem nome

Revision ID: 32a340dd9a4a
Revises: f6bb77fc9767
Create Date: 2025-06-06 16:56:59.958832

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32a340dd9a4a'
down_revision: Union[str, None] = 'f6bb77fc9767'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('rfid', sa.String(255), nullable=False),
        sa.Column('nome', sa.String(255), nullable=False),
        sa.Column('ultima_leitura', sa.DateTime, nullable=False),
        sa.Column('nivel_acesso', sa.Integer, nullable=False),
        sa.Column('status', sa.String(255), nullable=False),
    )
    op.add_column('funcionario', sa.Column('nome', sa.String(255), nullable=True))
    pass


def downgrade() -> None:
    op.drop_table('tags')
    pass
