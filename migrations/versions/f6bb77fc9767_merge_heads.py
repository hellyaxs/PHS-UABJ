"""merge_heads

Revision ID: f6bb77fc9767
Revises: 21bab657a8d6, 571919c1738a
Create Date: 2025-06-06 10:12:34.685848

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6bb77fc9767'
down_revision: Union[str, None] = ('21bab657a8d6', '571919c1738a')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
