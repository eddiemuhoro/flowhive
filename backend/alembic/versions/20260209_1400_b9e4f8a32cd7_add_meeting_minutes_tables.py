"""add_meeting_minutes_tables

Revision ID: b9e4f8a32cd7
Revises: a8f3c9d21e45
Create Date: 2026-02-09 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b9e4f8a32cd7'
down_revision: Union[str, None] = 'a8f3c9d21e45'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create meeting_minutes table
    op.create_table(
        'meeting_minutes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('workspace_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('meeting_date', sa.Date(), nullable=False),
        sa.Column('meeting_time_start', sa.Time(), nullable=True),
        sa.Column('meeting_time_end', sa.Time(), nullable=True),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('attendees', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('agenda', sa.Text(), nullable=True),
        sa.Column('discussions', sa.Text(), nullable=True),
        sa.Column('decisions', sa.Text(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['updated_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_meeting_minutes_id'), 'meeting_minutes', ['id'], unique=False)
    op.create_index(op.f('ix_meeting_minutes_title'), 'meeting_minutes', ['title'], unique=False)
    op.create_index(op.f('ix_meeting_minutes_meeting_date'), 'meeting_minutes', ['meeting_date'], unique=False)

    # Create minute_attachments table
    op.create_table(
        'minute_attachments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('meeting_minute_id', sa.Integer(), nullable=False),
        sa.Column('cloudinary_public_id', sa.String(), nullable=False),
        sa.Column('cloudinary_url', sa.String(), nullable=False),
        sa.Column('resource_type', sa.String(), nullable=False),
        sa.Column('file_name', sa.String(), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('mime_type', sa.String(), nullable=False),
        sa.Column('uploaded_by', sa.Integer(), nullable=False),
        sa.Column('uploaded_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['meeting_minute_id'], ['meeting_minutes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['uploaded_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_minute_attachments_id'), 'minute_attachments', ['id'], unique=False)

    # Create minute_action_items table
    op.create_table(
        'minute_action_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('meeting_minute_id', sa.Integer(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('assigned_to', sa.Integer(), nullable=True),
        sa.Column('due_date', sa.Date(), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['assigned_to'], ['users.id'], ),
        sa.ForeignKeyConstraint(['meeting_minute_id'], ['meeting_minutes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_minute_action_items_id'), 'minute_action_items', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_minute_action_items_id'), table_name='minute_action_items')
    op.drop_table('minute_action_items')
    op.drop_index(op.f('ix_minute_attachments_id'), table_name='minute_attachments')
    op.drop_table('minute_attachments')
    op.drop_index(op.f('ix_meeting_minutes_meeting_date'), table_name='meeting_minutes')
    op.drop_index(op.f('ix_meeting_minutes_title'), table_name='meeting_minutes')
    op.drop_index(op.f('ix_meeting_minutes_id'), table_name='meeting_minutes')
    op.drop_table('meeting_minutes')
