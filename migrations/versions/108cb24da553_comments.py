"""comments

Revision ID: 108cb24da553
Revises: 083fa7df76d7
Create Date: 2019-05-04 18:17:43.360598

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '108cb24da553'
down_revision = '083fa7df76d7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('default', sa.Boolean(), nullable=True),
    sa.Column('permissinons', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_roles_default'), 'roles', ['default'], unique=False)
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    # sa.Column('body_html', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comments_timestamp'), 'comments', ['timestamp'], unique=False)
    op.add_column('post', sa.Column('bod_html', sa.Text(), nullable=True))
    op.add_column('user', sa.Column('role_id', sa.Integer(), nullable=True))
    # op.create_foreign_key(None, 'user', 'roles', ['role_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'role_id')
    op.drop_column('post', 'bod_html')
    op.drop_index(op.f('ix_comments_timestamp'), table_name='comments')
    op.drop_table('comments')
    op.drop_index(op.f('ix_roles_default'), table_name='roles')
    op.drop_table('roles')
    # ### end Alembic commands ###
