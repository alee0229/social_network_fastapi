"""create content column in post

Revision ID: 8006f2bffa7e
Revises: 338a64f70a25
Create Date: 2022-03-30 22:27:20.556677

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8006f2bffa7e'
down_revision = '338a64f70a25'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts",sa.Column("content", sa.String(), nullable=False))

    pass


def downgrade():
    op.drop_column("posts","content")
    pass
