"""Add created_at to listings

Revision ID: 004
Revises: 003
Create Date: 2025-09-21 23:48:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add created_at column to listings
    op.add_column('listings', sa.Column('created_at', sa.DateTime(), nullable=True))
    # Set default value for existing rows
    op.execute("UPDATE listings SET created_at = NOW() WHERE created_at IS NULL")
    # Make it not nullable
    op.alter_column('listings', 'created_at', nullable=False)


def downgrade() -> None:
    # Remove created_at column from listings
    op.drop_column('listings', 'created_at')