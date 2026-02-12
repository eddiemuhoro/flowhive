"""remove_role_from_workspace_members

Revision ID: 9f26d9b32887
Revises: e9dc74224572
Create Date: 2026-02-12 15:02:10.273291

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f26d9b32887'
down_revision: Union[str, None] = 'e9dc74224572'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the role column from workspace_members table
    op.drop_column('workspace_members', 'role')


def downgrade() -> None:
    # Re-add the role column if we need to rollback
    op.add_column('workspace_members',
        sa.Column('role', sa.String(), nullable=False, server_default='member')
    )
