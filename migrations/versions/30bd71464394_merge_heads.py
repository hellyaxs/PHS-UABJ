"""merge_heads

Revision ID: 30bd71464394
Revises: 98ec0f811ee9, a4b32f0ce908
Create Date: 2025-06-04 15:59:19.562846

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '30bd71464394'
down_revision: Union[str, None] = ('98ec0f811ee9', 'a4b32f0ce908')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
