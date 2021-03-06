"""add foreign key to posts table

Revision ID: 11cf9081a761
Revises: 9ff183fb12b9
Create Date: 2022-03-30 22:45:06.874208

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11cf9081a761'
down_revision = '9ff183fb12b9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key("post_users_fk", source_table="posts", referent_table="users",
                        local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk',table_name="posts")
    op.drop_column("posts",'owner_id')
    pass
