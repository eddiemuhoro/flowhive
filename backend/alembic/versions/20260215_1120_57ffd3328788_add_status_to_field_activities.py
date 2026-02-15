"""add_status_to_field_activities

Revision ID: 57ffd3328788
Revises: 2ca2be3ed299
Create Date: 2026-02-15 11:20:02.884046

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '57ffd3328788'
down_revision: Union[str, None] = '2ca2be3ed299'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add status enum type
    op.execute("CREATE TYPE activitystatus AS ENUM ('PENDING', 'IN_PROGRESS', 'COMPLETED')")

    # Add status column with default COMPLETED for existing records
    op.add_column('field_activities', sa.Column('status', sa.Enum('PENDING', 'IN_PROGRESS', 'COMPLETED', name='activitystatus'), nullable=False, server_default='COMPLETED'))

    # Make start_time, end_time, task_description nullable
    op.alter_column('field_activities', 'start_time', nullable=True)
    op.alter_column('field_activities', 'end_time', nullable=True)
    op.alter_column('field_activities', 'task_description', nullable=True)


def downgrade() -> None:
    # Revert columns back to not nullable
    op.alter_column('field_activities', 'task_description', nullable=False)
    op.alter_column('field_activities', 'end_time', nullable=False)
    op.alter_column('field_activities', 'start_time', nullable=False)

    # Drop status column
    op.drop_column('field_activities', 'status')

    # Drop enum type
    op.execute("DROP TYPE activitystatus")
