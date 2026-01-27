"""add_title_to_field_activities

Revision ID: 4b7f7460fd16
Revises: bbba4ead3a4c
Create Date: 2026-01-27 17:56:31.606638

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b7f7460fd16'
down_revision: Union[str, None] = 'bbba4ead3a4c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add title column to field_activities
    op.add_column('field_activities',
        sa.Column('title', sa.String(), nullable=False, server_default='Untitled')
    )
    # Remove server default after adding the column
    op.alter_column('field_activities', 'title', server_default=None)


def downgrade() -> None:
    # Remove title column
    op.drop_column('field_activities', 'title')
