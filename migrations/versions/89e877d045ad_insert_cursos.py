"""insert_cursos

Revision ID: 89e877d045ad
Revises: 0311a3e2508f
Create Date: 2024-03-19 11:02:44.123456

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '89e877d045ad'
down_revision: Union[str, None] = '0311a3e2508f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Inserindo quatro cursos de engenharia
    op.execute("""
        INSERT INTO curso (nome) VALUES 
        ('Engenharia da Computação'),
        ('Engenharia de Controle e Automação'),
        ('Engenharia Hídrica'),
        ('Engenharia Química')
    """)


def downgrade() -> None:
    # Removendo os cursos inseridos
    op.execute("""
        DELETE FROM curso WHERE nome IN (
            'Engenharia da Computação',
            'Engenharia de Controle e Automação',
            'Engenharia Hídrica',
            'Engenharia Química'
        )
    """)
