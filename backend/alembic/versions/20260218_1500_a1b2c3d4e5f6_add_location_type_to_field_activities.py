"""add_location_type_to_field_activities

Revision ID: a1b2c3d4e5f6
Revises: 57ffd3328788
Create Date: 2026-02-18 15:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '57ffd3328788'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the enum type
    location_type_enum = sa.Enum('OFFICE', 'ON_SITE', name='locationtype')
    location_type_enum.create(op.get_bind(), checkfirst=True)

    # Add location_type column to field_activities table with default value
    # Default to OFFICE as most existing activities were done in office
    op.add_column('field_activities',
        sa.Column('location_type', location_type_enum,
                  nullable=False, server_default='OFFICE'))

    # Create index for better query performance
    op.create_index('ix_field_activities_location_type', 'field_activities', ['location_type'])


def downgrade() -> None:
    # Drop the index
    op.drop_index('ix_field_activities_location_type', table_name='field_activities')

    # Drop the column
    op.drop_column('field_activities', 'location_type')

    # Drop the enum type
    sa.Enum(name='locationtype').drop(op.get_bind(), checkfirst=True)
