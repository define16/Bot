"""create chosun news table

Revision ID: d395020e4990
Revises: 
Create Date: 2020-08-30 13:52:10.008331

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd395020e4990'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'chosun_news',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('title', sa.String(30)),
        sa.Column('wrote_at', sa.String(30)),
        sa.Column('body', sa.String(30)),
        sa.Column('created_at', sa.DateTime(6), server_default=sa.sql.func.now()),
        sa.Column('updated_at', sa.DateTime(6), onupdate=sa.sql.func.now())
    )


def downgrade():
    pass
