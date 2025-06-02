"""insert cursos

Revision ID: 2a39b4318a28
Revises: 
Create Date: 2025-06-01 12:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2a39b4318a28'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.bulk_insert(
        sa.table('curso',
                 sa.column('nome', sa.String(length=150))
                 ),
        [
            {'nome': 'Engenharia da Computação'},
            {'nome': 'Engenharia Hídrica'},
            {'nome': 'Engenharia Química'},
            {'nome': 'Engenharia de Controle e Automação'},
        ]
    )


def downgrade():
    op.execute("""
        DELETE FROM curso WHERE nome IN (
            'Engenharia da Computação',
            'Engenharia Hídrica',
            'Engenharia Química',
            'Engenharia de Controle e Automação'
        )
    """)
