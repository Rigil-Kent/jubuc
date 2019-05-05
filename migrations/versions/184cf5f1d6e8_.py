"""empty message

Revision ID: 184cf5f1d6e8
Revises: 
Create Date: 2019-05-05 17:44:42.790813

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '184cf5f1d6e8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('administrator',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('first_name', sa.String(length=64), nullable=True),
    sa.Column('last_name', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=256), nullable=True),
    sa.Column('pass_hash', sa.String(length=128), nullable=True),
    sa.Column('site_title', sa.String(length=64), nullable=True),
    sa.Column('site_logo_text', sa.String(length=28), nullable=True),
    sa.Column('site_logo_image', sa.String(length=256), nullable=True),
    sa.Column('jumbotron_image', sa.String(length=256), nullable=True),
    sa.Column('site_dominant_color', sa.String(), nullable=True),
    sa.Column('site_accent_color', sa.String(), nullable=True),
    sa.Column('site_background_color', sa.String(), nullable=True),
    sa.Column('facebook', sa.String(length=128), nullable=True),
    sa.Column('twitter', sa.String(length=128), nullable=True),
    sa.Column('instagram', sa.String(length=128), nullable=True),
    sa.Column('soundcloud', sa.String(length=128), nullable=True),
    sa.Column('youtube', sa.String(length=128), nullable=True),
    sa.Column('spotify', sa.String(length=128), nullable=True),
    sa.Column('twitter_consumer_key', sa.String(length=256), nullable=True),
    sa.Column('twitter_consumer_key_secret', sa.String(length=256), nullable=True),
    sa.Column('twitter_access_token', sa.String(length=256), nullable=True),
    sa.Column('twitter_access_token_secret', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_administrator_timestamp'), 'administrator', ['timestamp'], unique=False)
    op.create_index(op.f('ix_administrator_username'), 'administrator', ['username'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('first_name', sa.String(length=64), nullable=True),
    sa.Column('last_name', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=256), nullable=True),
    sa.Column('pass_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_timestamp'), 'user', ['timestamp'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_timestamp'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_administrator_username'), table_name='administrator')
    op.drop_index(op.f('ix_administrator_timestamp'), table_name='administrator')
    op.drop_table('administrator')
    # ### end Alembic commands ###
