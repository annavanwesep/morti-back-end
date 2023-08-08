"""recreated user and message model

Revision ID: 9059ee38b431
Revises: 
Create Date: 2023-08-07 16:59:25.550039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9059ee38b431'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=345), nullable=True),
    sa.Column('password', sa.Text(), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=True),
    sa.Column('last_name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('message',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=50), nullable=True),
    sa.Column('text_message', sa.String(length=500), nullable=True),
    sa.Column('audio_message', sa.String(), nullable=True),
    sa.Column('recipient_email', sa.String(length=345), nullable=True),
    sa.Column('recipient_id', sa.Integer(), nullable=True),
    sa.Column('is_sent', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('message')
    op.drop_table('user')
    # ### end Alembic commands ###
