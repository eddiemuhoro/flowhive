"""add_customer_id_to_field_activities

Revision ID: 2ca2be3ed299
Revises: 46e74243f75c
Create Date: 2026-02-14 12:44:22.744587

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ca2be3ed299'
down_revision: Union[str, None] = '46e74243f75c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add customer_id column to field_activities table
    op.add_column('field_activities', sa.Column('customer_id', sa.String(), nullable=True))


def downgrade() -> None:
    # Remove customer_id column from field_activities table
    op.drop_column('field_activities', 'customer_id')
