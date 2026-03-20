"""add field activity comments

Revision ID: 4d2f8c1a9b77
Revises: fd5cc061bc97
Create Date: 2026-03-20 21:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d2f8c1a9b77'
down_revision: Union[str, None] = 'fd5cc061bc97'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'field_activity_comments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('field_activity_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('parent_comment_id', sa.Integer(), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['field_activity_id'], ['field_activities.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['parent_comment_id'], ['field_activity_comments.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_field_activity_comments_field_activity_id'), 'field_activity_comments', ['field_activity_id'], unique=False)
    op.create_index(op.f('ix_field_activity_comments_id'), 'field_activity_comments', ['id'], unique=False)
    op.create_index(op.f('ix_field_activity_comments_user_id'), 'field_activity_comments', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_field_activity_comments_user_id'), table_name='field_activity_comments')
    op.drop_index(op.f('ix_field_activity_comments_id'), table_name='field_activity_comments')
    op.drop_index(op.f('ix_field_activity_comments_field_activity_id'), table_name='field_activity_comments')
    op.drop_table('field_activity_comments')
