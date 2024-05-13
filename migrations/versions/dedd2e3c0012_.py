"""empty message

Revision ID: dedd2e3c0012
Revises: 1e5c35d1ad2f
Create Date: 2024-05-12 23:43:36.546521

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dedd2e3c0012'
down_revision = '6275cacc4efa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.String(length=128), nullable=True))
        batch_op.drop_column('password')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.VARCHAR(length=60), nullable=False))
        batch_op.drop_column('password_hash')

    # ### end Alembic commands ###
