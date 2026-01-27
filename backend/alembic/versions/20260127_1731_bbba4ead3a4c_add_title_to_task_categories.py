"""add_title_to_task_categories

Revision ID: bbba4ead3a4c
Revises: fe711eec93bf
Create Date: 2026-01-27 17:31:57.393988

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bbba4ead3a4c'
down_revision: Union[str, None] = 'fe711eec93bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add title column to task_categories
    op.add_column('task_categories',
        sa.Column('title', sa.String(), nullable=False, server_default='Untitled')
    )
    # Remove server default after adding the column
    op.alter_column('task_categories', 'title', server_default=None)


def downgrade() -> None:
    # Remove title column
    op.drop_column('task_categories', 'title')
