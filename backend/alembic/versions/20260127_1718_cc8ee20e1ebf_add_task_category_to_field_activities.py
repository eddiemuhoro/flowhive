"""add_task_category_to_field_activities

Revision ID: cc8ee20e1ebf
Revises: e40aa9b5c0d6
Create Date: 2026-01-27 17:18:01.985558

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc8ee20e1ebf'
down_revision: Union[str, None] = 'e40aa9b5c0d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create task_category enum
    task_category_enum = sa.Enum(
        'INSTALLATION', 
        'MAINTENANCE', 
        'REPAIR', 
        'INSPECTION', 
        'TRAINING', 
        'SURVEY',
        'CONSULTATION',
        'EMERGENCY',
        'OTHER',
        name='taskcategory'
    )
    task_category_enum.create(op.get_bind())
    
    # Add task_category column to field_activities table
    op.add_column('field_activities', 
        sa.Column('task_category', task_category_enum, nullable=True)
    )
    op.create_index(op.f('ix_field_activities_task_category'), 'field_activities', ['task_category'], unique=False)


def downgrade() -> None:
    # Remove task_category column
    op.drop_index(op.f('ix_field_activities_task_category'), table_name='field_activities')
    op.drop_column('field_activities', 'task_category')
    
    # Drop task_category enum
    sa.Enum(name='taskcategory').drop(op.get_bind())
