"""create post table

Revision ID: 338a64f70a25
Revises: 
Create Date: 2022-03-30 22:21:44.166423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '338a64f70a25'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts", sa.Column('id',sa.Integer(), nullable=False, primary_key=True),
                             sa.Column('title',sa.String(),nullable=False)   
                                )
    pass


def downgrade():
    op.drop_table('posts')
    pass
