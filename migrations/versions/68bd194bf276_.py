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
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('isvalid', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###


    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('isvalid')


    # ### end Alembic commands ###
