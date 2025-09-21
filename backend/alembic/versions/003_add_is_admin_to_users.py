"""add is_admin to users

Revision ID: 003
Revises: 002
Create Date: 2025-09-21 22:09:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add is_admin column to users table
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=False, default=False))


def downgrade() -> None:
    # Remove is_admin column from users table
    op.drop_column('users', 'is_admin')