"""..

Revision ID: 68bd194bf276
Revises: 2ba4eb646685
Create Date: 2019-05-07 00:36:12.481057

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '68bd194bf276'
down_revision = '2ba4eb646685'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles')
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('isvalid', sa.Boolean(), nullable=True))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('user_ibfk_1', type_='foreignkey')
        batch_op.drop_column('role_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('user_ibfk_1', 'roles', ['role_id'], ['id'])

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('isvalid')

    op.create_table('roles',
    sa.Column('id', mysql.INTEGER(display_width=10), autoincrement=False, nullable=False),
    sa.Column('name', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=64), nullable=True),
    sa.Column('default', mysql.TINYINT(display_width=1), server_default=sa.text("'0'"), autoincrement=False, nullable=True),
    sa.Column('permissions', mysql.INTEGER(display_width=10), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
