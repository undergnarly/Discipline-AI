"""add google oauth fields

Revision ID: add_google_oauth_fields
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_google_oauth_fields'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Добавляем новые колонки для Google OAuth
    op.add_column('users', sa.Column('google_id', sa.String(), nullable=True))
    op.add_column('users', sa.Column('google_email', sa.String(), nullable=True))
    op.add_column('users', sa.Column('google_picture', sa.String(), nullable=True))
    op.add_column('users', sa.Column('google_access_token', sa.String(), nullable=True))
    op.add_column('users', sa.Column('google_refresh_token', sa.String(), nullable=True))
    op.add_column('users', sa.Column('google_token_expiry', sa.DateTime(), nullable=True))
    
    # Создаем уникальные индексы
    op.create_index(op.f('ix_users_google_id'), 'users', ['google_id'], unique=True)
    op.create_index(op.f('ix_users_google_email'), 'users', ['google_email'], unique=True)

def downgrade():
    # Удаляем индексы
    op.drop_index(op.f('ix_users_google_email'), table_name='users')
    op.drop_index(op.f('ix_users_google_id'), table_name='users')
    
    # Удаляем колонки
    op.drop_column('users', 'google_token_expiry')
    op.drop_column('users', 'google_refresh_token')
    op.drop_column('users', 'google_access_token')
    op.drop_column('users', 'google_picture')
    op.drop_column('users', 'google_email')
    op.drop_column('users', 'google_id') 