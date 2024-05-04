"""Add table acess_tokens

Revision ID: 37e18e3672ae
Revises: 853a3973d462
Create Date: 2024-04-26 00:24:51.597638

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37e18e3672ae'
down_revision: Union[str, None] = '853a3973d462'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'access_tokens',
        sa.Column('key', sa.String(128), primary_key=True),
        sa.Column('created', sa.DateTime(), server_default=sa.func.now(), server_onupdate=sa.func.now(), nullable=False),
        sa.Column('user_id', sa.Uuid(), sa.ForeignKey('users.id', ondelete='CASCADE'), unique=True, index=True, nullable=False)
    )


def downgrade() -> None:
    op.drop_table('access_tokens')

