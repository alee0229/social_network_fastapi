"""add last columns to post table

Revision ID: 4f6537c2566e
Revises: 11cf9081a761
Create Date: 2022-03-30 22:53:42.765695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f6537c2566e'
down_revision = '11cf9081a761'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
                    sa.Column("published", sa.Boolean(),nullable=False, server_default='TRUE'))

    op.add_column('posts',
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True),nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts',
                    'published')

    op.drop_column('posts',
                    'created_at'    )
    pass
