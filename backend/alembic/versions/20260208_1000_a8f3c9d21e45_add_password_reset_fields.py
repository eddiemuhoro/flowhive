"""add_password_reset_fields

Revision ID: a8f3c9d21e45
Revises: 4b7f7460fd16
Create Date: 2026-02-08 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8f3c9d21e45'
down_revision: Union[str, None] = '4b7f7460fd16'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add password reset fields to users table
    op.add_column('users', sa.Column('reset_token', sa.String(), nullable=True))
    op.add_column('users', sa.Column('reset_token_expires', sa.DateTime(), nullable=True))


def downgrade() -> None:
    # Remove password reset fields
    op.drop_column('users', 'reset_token_expires')
    op.drop_column('users', 'reset_token')
