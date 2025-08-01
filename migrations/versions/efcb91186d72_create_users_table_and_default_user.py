"""create_users_table_and_default_user

Revision ID: efcb91186d72
Revises: be2ac0b6d6db
Create Date: 2025-07-27 19:00:20.987190

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import func, table, column
from src.infra.config.settings import user_settings

# revision identifiers, used by Alembic.
revision: str = 'efcb91186d72'
down_revision: Union[str, None] = 'be2ac0b6d6db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    op.create_table('users',
        sa.Column('email', sa.String, primary_key=True),
        sa.Column('hashed_password', sa.String, nullable=False),
        sa.Column('full_name', sa.String),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=func.now())
    )
    op.bulk_insert(
        sa.table('users',
            sa.column('email', sa.String),
            sa.column('hashed_password', sa.String),
            sa.column('full_name', sa.String),
            sa.column('is_active', sa.Boolean)
        ),
        [
            {
                'email': user_settings.DEFAULT_USER_EMAIL,
                'hashed_password': user_settings.get_hashed_password(),
                'full_name': user_settings.DEFAULT_USER_FULL_NAME,
                'is_active': user_settings.DEFAULT_USER_IS_ACTIVE
            }
        ]
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.execute(
        sa.text(f"DELETE FROM users WHERE email = '{user_settings.DEFAULT_USER_EMAIL}'")
    )
    # ### end Alembic commands ###
