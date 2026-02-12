"""add_role_to_workspace_members

Revision ID: f8438d441891
Revises: b9e4f8a32cd7
Create Date: 2026-02-12 14:31:32.998396

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8438d441891'
down_revision: Union[str, None] = 'b9e4f8a32cd7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add role column to workspace_members table
    op.add_column('workspace_members', sa.Column('role', sa.String(), nullable=True))
    # Set default role for existing members as 'member'
    op.execute("UPDATE workspace_members SET role = 'member' WHERE role IS NULL")
    # Make role non-nullable after setting defaults
    op.alter_column('workspace_members', 'role', nullable=False, server_default='member')


def downgrade() -> None:
    # Remove role column from workspace_members table
    op.drop_column('workspace_members', 'role')
