"""convert_task_category_to_table

Revision ID: fe711eec93bf
Revises: cc8ee20e1ebf
Create Date: 2026-01-27 17:28:36.964544

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe711eec93bf'
down_revision: Union[str, None] = 'cc8ee20e1ebf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create task_categories table
    op.create_table('task_categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('color', sa.String(), nullable=True),
        sa.Column('icon', sa.String(), nullable=True),
        sa.Column('workspace_id', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_categories_id'), 'task_categories', ['id'], unique=False)
    op.create_index(op.f('ix_task_categories_workspace_id'), 'task_categories', ['workspace_id'], unique=False)
    
    # Drop the old task_category enum column from field_activities
    op.drop_index(op.f('ix_field_activities_task_category'), table_name='field_activities')
    op.drop_column('field_activities', 'task_category')
    
    # Drop the enum type
    sa.Enum(name='taskcategory').drop(op.get_bind())
    
    # Add task_category_id foreign key column to field_activities
    op.add_column('field_activities',
        sa.Column('task_category_id', sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        'fk_field_activities_task_category',
        'field_activities', 'task_categories',
        ['task_category_id'], ['id']
    )
    op.create_index(op.f('ix_field_activities_task_category_id'), 'field_activities', ['task_category_id'], unique=False)


def downgrade() -> None:
    # Remove task_category_id from field_activities
    op.drop_index(op.f('ix_field_activities_task_category_id'), table_name='field_activities')
    op.drop_constraint('fk_field_activities_task_category', 'field_activities', type_='foreignkey')
    op.drop_column('field_activities', 'task_category_id')
    
    # Recreate the enum
    task_category_enum = sa.Enum(
        'INSTALLATION', 'MAINTENANCE', 'REPAIR', 'INSPECTION', 
        'TRAINING', 'SURVEY', 'CONSULTATION', 'EMERGENCY', 'OTHER',
        name='taskcategory'
    )
    task_category_enum.create(op.get_bind())
    
    # Add back the enum column
    op.add_column('field_activities',
        sa.Column('task_category', task_category_enum, nullable=True)
    )
    op.create_index(op.f('ix_field_activities_task_category'), 'field_activities', ['task_category'], unique=False)
    
    # Drop task_categories table
    op.drop_index(op.f('ix_task_categories_workspace_id'), table_name='task_categories')
    op.drop_index(op.f('ix_task_categories_id'), table_name='task_categories')
    op.drop_table('task_categories')
