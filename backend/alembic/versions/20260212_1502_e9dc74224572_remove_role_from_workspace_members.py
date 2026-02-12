"""remove_role_from_workspace_members

Revision ID: e9dc74224572
Revises: f8438d441891
Create Date: 2026-02-12 15:02:01.671991

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e9dc74224572'
down_revision: Union[str, None] = 'f8438d441891'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
