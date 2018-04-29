"""empty message

Revision ID: 0001_create_site_table
Revises:
Create Date: 2018-04-29 18:19:29.819578

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_create_site_table'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('site',
                    sa.Column('id', sa.Integer(), nullable=False, server_default=sa.null()),
                    sa.Column('name', sa.String(length=100), nullable=False),
                    sa.Column('latitude', sa.Float()),
                    sa.Column('longitude', sa.Float()),
                    sa.Column('elevation', sa.Float()),
                    sa.Column('region', sa.String(length=100)),
                    sa.Column('unitary_auth_area', sa.String(length=100)),
                    sa.Column('obs_source', sa.String(length=100)),
                    sa.Column('national_park', sa.String(length=100)),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_site_name'), 'site', ['name'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_site_name'), table_name='site')
    op.drop_table('site')
