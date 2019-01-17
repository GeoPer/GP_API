"""empty message

Revision ID: dc43a631ec1e
Revises: 09e61e6e23b6
Create Date: 2018-12-11 18:33:05.602566

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'dc43a631ec1e'
down_revision = '09e61e6e23b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('area', sa.Column('lon', sa.Float(), nullable=False))
    op.drop_column('area', 'long')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('area', sa.Column('long', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.drop_column('area', 'lon')
    # ### end Alembic commands ###