"""add last few columns to posts table

Revision ID: 161f27cafc5d
Revises: 99b6c3055b04
Create Date: 2023-02-11 17:00:45.887104

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '161f27cafc5d'
down_revision = '99b6c3055b04'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=True, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
