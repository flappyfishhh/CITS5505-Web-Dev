"""merging two heads

Revision ID: ed30f4329543
Revises: 1e5c35d1ad2f, dedd2e3c0012
Create Date: 2024-05-13 00:28:29.364295

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed30f4329543'
down_revision = ('1e5c35d1ad2f', 'dedd2e3c0012')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
