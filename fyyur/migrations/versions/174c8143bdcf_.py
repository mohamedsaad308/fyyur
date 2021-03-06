"""empty message

Revision ID: 174c8143bdcf
Revises: 184fd182c207
Create Date: 2020-10-20 00:17:23.657150

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '174c8143bdcf'
down_revision = '184fd182c207'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    op.drop_column('Artist', 'seeking_talent')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('seeking_talent', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('Artist', 'seeking_venue')
    # ### end Alembic commands ###
