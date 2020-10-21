"""empty message

Revision ID: d0b9742f0c04
Revises: 4412e3364048
Create Date: 2020-10-19 14:29:53.532131

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0b9742f0c04'
down_revision = '4412e3364048'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('genres', sa.String(length=120), nullable=True))
    op.add_column('Venue', sa.Column('seeking_description', sa.String(length=120), nullable=True))
    op.add_column('Venue', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    op.add_column('Venue', sa.Column('website', sa.String(length=120), nullable=True))
    op.create_unique_constraint(None, 'Venue', ['city'])
    op.create_unique_constraint(None, 'Venue', ['state'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Venue', type_='unique')
    op.drop_constraint(None, 'Venue', type_='unique')
    op.drop_column('Venue', 'website')
    op.drop_column('Venue', 'seeking_talent')
    op.drop_column('Venue', 'seeking_description')
    op.drop_column('Venue', 'genres')
    # ### end Alembic commands ###