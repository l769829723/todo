"""empty message

Revision ID: daa04b188c83
Revises: 432fb49d2df1
Create Date: 2018-08-21 12:53:33.771146

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'daa04b188c83'
down_revision = '432fb49d2df1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blog_channels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('blog_posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('channel', sa.String(length=128), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('publish_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['channel'], ['blog_channels.name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_blog_posts_name'), 'blog_posts', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_blog_posts_name'), table_name='blog_posts')
    op.drop_table('blog_posts')
    op.drop_table('blog_channels')
    # ### end Alembic commands ###
