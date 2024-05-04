"""Add tables users, job_ositions and user_job_position

Revision ID: 853a3973d462
Revises: 
Create Date: 2024-04-25 19:03:36.104355

"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '853a3973d462'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Uuid(), primary_key=True, default=uuid.uuid4),
        sa.Column('username', sa.String(128), unique=True, index=True, nullable=False),
        sa.Column('password', sa.String(128),nullable=False),
        sa.Column('first_name', sa.String(150), nullable=False),
        sa.Column('last_name', sa.String(150), nullable=False),
        sa.Column('date_of_employment', sa.Date(), server_default=sa.func.now(), nullable=False),  
        sa.Column('is_superuser', sa.Boolean(), index=True, default=False, nullable=False),
        sa.Column('is_staff', sa.Boolean(), index=True, default=True, nullable=False)
    )

    op.create_table(
        'jobs',
        sa.Column('id', sa.Uuid(), primary_key=True, default=uuid.uuid4),
        sa.Column('title', sa.String(150), nullable=False),
        sa.Column('salary', sa.Numeric(), nullable=False),
        sa.Column('days_to_promotion', sa.Interval(), nullable=False),
    )

    op.create_table(
        'user_job',
        sa.Column('id', sa.Uuid(), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', sa.Uuid(), sa.ForeignKey('users.id', ondelete='CASCADE'), unique=True, index=True, nullable=False),
        sa.Column('job_id', sa.Uuid(), sa.ForeignKey('jobs.id', ondelete='CASCADE'), index=True, nullable=False)
    )


def downgrade() -> None:
    op.drop_table('user_job')
    op.drop_table('jobs')
    op.drop_table('users')

