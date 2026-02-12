"""add_created_by_to_task_categories

Revision ID: 46e74243f75c
Revises: 96df6da64fe8
Create Date: 2026-02-12 19:44:07.746551

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46e74243f75c'
down_revision: Union[str, None] = '96df6da64fe8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add created_by column to task_categories table
    op.add_column('task_categories', sa.Column('created_by', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_task_categories_created_by', 'task_categories', 'users', ['created_by'], ['id'])


def downgrade() -> None:
    # Remove created_by column from task_categories table
    op.drop_constraint('fk_task_categories_created_by', 'task_categories', type_='foreignkey')
    op.drop_column('task_categories', 'created_by')
