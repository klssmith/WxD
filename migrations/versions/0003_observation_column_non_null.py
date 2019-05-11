"""empty message

Revision ID: 0003_observation_column_non_null
Revises: 0002_add_site_observation_column
Create Date: 2019-05-11 20:36:38.380758

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0003_observation_column_non_null'
down_revision = '0002_add_site_observation_column'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('site', 'observations', existing_type=sa.BOOLEAN(), nullable=False)


def downgrade():
    op.alter_column('site', 'observations', existing_type=sa.BOOLEAN(), nullable=True)
