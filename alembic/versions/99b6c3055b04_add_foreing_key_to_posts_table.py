"""add foreing-key to posts table

Revision ID: 99b6c3055b04
Revises: cb49d13ccd56
Create Date: 2023-02-11 16:34:51.167870

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99b6c3055b04'
down_revision = 'cb49d13ccd56'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users", local_cols=['owner_id'],
                          remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_column('posts', 'owner_id')
    op.drop_constraint('posts_users_fk', table_name='posts')
    pass
