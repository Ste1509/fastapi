"""add content column to posts table

Revision ID: fe721e6bef99
Revises: 00fd9485a9e5
Create Date: 2023-02-11 15:40:47.101132

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe721e6bef99'
down_revision = '00fd9485a9e5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False ))
    pass


def downgrade() -> None:
    op.add_column('posts', 'content')
    pass
