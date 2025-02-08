"""initialize

Revision ID: c0b9fbbfb9d2
Revises: 
Create Date: 2025-02-06 11:41:38.506127

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0b9fbbfb9d2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create the "users" table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('date_created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('username', sa.String(), unique=True, nullable=True),
        sa.Column('password', sa.String(), unique=True, nullable=True)
    )
    # Create an index on the "name" column (as specified in the model)
    op.create_index('ix_users_name', 'users', ['name'])

    # Create the "user_photos" table
    op.create_table(
        'user_photos',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('username', sa.String(), nullable=True),
        sa.Column('file_url', sa.String(), nullable=True),
        sa.Column('user_filename', sa.String(), nullable=True),
        sa.Column('date_created', sa.DateTime(), server_default=sa.text('now()'), nullable=False)
    )


def downgrade():
    # Drop the "user_photos" table first
    op.drop_table('user_photos')
    # Drop the index on the "users" table and then the table itself
    op.drop_index('ix_users_name', table_name='users')
    op.drop_table('users')