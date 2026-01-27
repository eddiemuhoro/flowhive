"""add_field_operations_tables

Revision ID: e40aa9b5c0d6
Revises: 117e2b415849
Create Date: 2026-01-27 16:56:43.152995

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e40aa9b5c0d6'
down_revision: Union[str, None] = '117e2b415849'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create workspace_type enum
    workspace_type_enum = sa.Enum('PROJECT_MANAGEMENT', 'FIELD_OPERATIONS', name='workspacetype')
    workspace_type_enum.create(op.get_bind())
    
    # Add workspace_type column to workspaces table
    op.add_column('workspaces', 
        sa.Column('workspace_type', workspace_type_enum, nullable=False, server_default='PROJECT_MANAGEMENT')
    )
    op.create_index(op.f('ix_workspaces_workspace_type'), 'workspaces', ['workspace_type'], unique=False)
    
    # Create field_activities table
    op.create_table('field_activities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('workspace_id', sa.Integer(), nullable=False),
        sa.Column('support_staff_id', sa.Integer(), nullable=False),
        sa.Column('activity_date', sa.Date(), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=False),
        sa.Column('end_time', sa.Time(), nullable=False),
        sa.Column('customer_name', sa.String(), nullable=False),
        sa.Column('location', sa.String(), nullable=False),
        sa.Column('task_description', sa.Text(), nullable=False),
        sa.Column('remarks', sa.Text(), nullable=True),
        sa.Column('customer_rep', sa.String(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=False),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ),
        sa.ForeignKeyConstraint(['support_staff_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['updated_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_field_activities_id'), 'field_activities', ['id'], unique=False)
    op.create_index(op.f('ix_field_activities_activity_date'), 'field_activities', ['activity_date'], unique=False)
    op.create_index(op.f('ix_field_activities_support_staff_id'), 'field_activities', ['support_staff_id'], unique=False)
    
    # Create field_activity_photos table
    op.create_table('field_activity_photos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('field_activity_id', sa.Integer(), nullable=False),
        sa.Column('file_path', sa.String(), nullable=False),
        sa.Column('file_name', sa.String(), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('mime_type', sa.String(), nullable=False),
        sa.Column('uploaded_by', sa.Integer(), nullable=False),
        sa.Column('uploaded_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['field_activity_id'], ['field_activities.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['uploaded_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_field_activity_photos_id'), 'field_activity_photos', ['id'], unique=False)


def downgrade() -> None:
    # Drop field_activity_photos table
    op.drop_index(op.f('ix_field_activity_photos_id'), table_name='field_activity_photos')
    op.drop_table('field_activity_photos')
    
    # Drop field_activities table
    op.drop_index(op.f('ix_field_activities_support_staff_id'), table_name='field_activities')
    op.drop_index(op.f('ix_field_activities_activity_date'), table_name='field_activities')
    op.drop_index(op.f('ix_field_activities_id'), table_name='field_activities')
    op.drop_table('field_activities')
    
    # Remove workspace_type column from workspaces
    op.drop_index(op.f('ix_workspaces_workspace_type'), table_name='workspaces')
    op.drop_column('workspaces', 'workspace_type')
    
    # Drop workspace_type enum
    sa.Enum(name='workspacetype').drop(op.get_bind())
