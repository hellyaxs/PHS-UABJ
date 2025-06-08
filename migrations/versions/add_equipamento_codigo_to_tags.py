"""add_equipamento_codigo_to_tags

Revision ID: add_equipamento_codigo_to_tags
Revises: 32a340dd9a4a
Create Date: 2025-06-05 13:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_equipamento_codigo_to_tags'
down_revision: Union[str, None] = '32a340dd9a4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Adiciona a coluna equipamento_codigo na tabela tags
    op.add_column('tags', sa.Column('equipamento_codigo', sa.String(50), nullable=True))
    
    # Adiciona a foreign key
    op.create_foreign_key(
        'fk_tags_equipamento',
        'tags', 'equipamento',
        ['equipamento_codigo'], ['codigo_tombamento']
    )


def downgrade() -> None:
    # Remove a foreign key
    op.drop_constraint('fk_tags_equipamento', 'tags', type_='foreignkey')
    
    # Remove a coluna
    op.drop_column('tags', 'equipamento_codigo') 