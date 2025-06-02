"""insert_cargos

Revision ID: 571919c1738a
Revises: 2a39b4318a28
Create Date: 2025-06-01 22:43:55.103627

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import table, column


# revision identifiers, used by Alembic.
revision: str = '571919c1738a'
down_revision: Union[str, None] = '2a39b4318a28'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    cargo_table = table('cargo',
                        column('id', sa.Integer),
                        column('nome', sa.String(100))
                       )
    
    op.bulk_insert(cargo_table, [
        {'id': 1, 'nome': 'Professor Titular'},
        {'id': 2, 'nome': 'Professor Associado'},
        {'id': 3, 'nome': 'Professor Adjunto'},
        {'id': 4, 'nome': 'Professor Assistente'},
        {'id': 5, 'nome': 'Professor Auxiliar'},
        {'id': 6, 'nome': 'Professor Substituto'},
        {'id': 7, 'nome': 'Coordenador de Curso'},
        {'id': 8, 'nome': 'Chefe de Departamento'},
        {'id': 9, 'nome': 'Diretor de Unidade'},
    ])


def downgrade() -> None:
    pass
