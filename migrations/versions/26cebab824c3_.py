"""empty message

Revision ID: 26cebab824c3
Revises: f42f87c11822
Create Date: 2020-02-01 03:09:52.515552

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26cebab824c3'
down_revision = 'f42f87c11822'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('incident', sa.Column('latitude', sa.Float(), nullable=False))
    op.create_unique_constraint(None, 'incident', ['latitude'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'incident', type_='unique')
    op.drop_column('incident', 'latitude')
    # ### end Alembic commands ###
