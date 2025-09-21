"""add server table and update listings

Revision ID: 002
Revises: 001
Create Date: 2025-09-21 21:50:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create servers table
    op.create_table('servers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('chronicle', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_servers_id'), 'servers', ['id'], unique=False)

    # Add server_id column to listings
    op.add_column('listings', sa.Column('server_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_listings_server_id', 'listings', 'servers', ['server_id'], ['id'])

    # Insert initial servers
    op.execute("""
    INSERT INTO servers (name, chronicle) VALUES
    ('Adena', 'Interlude'),
    ('Adena Classic', 'Interlude'),
    ('Adena High Five', 'High Five'),
    ('Adena Goddess of Destruction', 'Goddess of Destruction'),
    ('Adena Ertheia', 'Ertheia'),
    ('Adena Salvation', 'Salvation')
    """)

    # Update existing listings to use server_id based on server_name
    op.execute("""
    UPDATE listings SET server_id = (
        SELECT id FROM servers WHERE name = listings.server_name LIMIT 1
    ) WHERE server_name IS NOT NULL
    """)

    # Make server_id not nullable after data migration
    op.alter_column('listings', 'server_id', nullable=False)

    # Drop server_name column
    op.drop_column('listings', 'server_name')


def downgrade() -> None:
    # Add back server_name column
    op.add_column('listings', sa.Column('server_name', sa.String(), nullable=True))

    # Populate server_name from server_id
    op.execute("""
    UPDATE listings SET server_name = (
        SELECT name FROM servers WHERE id = listings.server_id
    ) WHERE server_id IS NOT NULL
    """)

    # Drop foreign key and server_id column
    op.drop_constraint('fk_listings_server_id', 'listings', type_='foreignkey')
    op.drop_column('listings', 'server_id')

    # Drop servers table
    op.drop_index(op.f('ix_servers_id'), table_name='servers')
    op.drop_table('servers')