"""empty message

Revision ID: 0002_add_site_observation_column
Revises: 0001_create_site_table
Create Date: 2018-05-06 17:54:34.882442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0002_add_site_observation_column'
down_revision = '0001_create_site_table'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('site', sa.Column('observations', sa.Boolean(), nullable=True))
    op.create_index(op.f('ix_site_observations'), 'site', ['observations'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_site_observations'), table_name='site')
    op.drop_column('site', 'observations')
