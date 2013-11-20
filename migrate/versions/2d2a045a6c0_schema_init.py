"""schema init

Revision ID: 2d2a045a6c0
Revises: None
Create Date: 2013-11-20 11:23:16.139647

"""

# revision identifiers, used by Alembic.
revision = '2d2a045a6c0'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('stage',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('display_name', sa.String(150), unique=True,
                              nullable=False),
                    sa.Column('quiz_name', sa.String(150), nullable=False),
                    sa.Column('prev_stage_id', sa.Integer,
                              sa.ForeignKey('stage.id'))
                    )

    op.create_table('record',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('session_id', sa.String(64), nullable=False),
                    sa.Column('stage_id', sa.Integer,
                              sa.ForeignKey('stage.id')),
                    sa.Column('key', sa.String(64), nullable=False,
                              unique=True),
                    sa.Column('next_record_id', sa.Integer,
                              sa.ForeignKey('record.id'))
                    )


def downgrade():
    op.drop_table('record')
    op.drop_table('stage')
