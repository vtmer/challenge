"""backend user

Revision ID: 3f4a469823fb
Revises: 2d2a045a6c0
Create Date: 2013-11-21 21:15:47.050947

"""

# revision identifiers, used by Alembic.
revision = '3f4a469823fb'
down_revision = '2d2a045a6c0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('auth',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('password', sa.String(64), nullable=False)
                    )


def downgrade():
    op.drop_table('auth')
