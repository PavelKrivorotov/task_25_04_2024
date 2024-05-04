"""Insert table job_positions

Revision ID: 3d8dfa8405d9
Revises: 37e18e3672ae
Create Date: 2024-04-26 00:31:37.594319

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from job.models import Job


# revision identifiers, used by Alembic.
revision: str = '3d8dfa8405d9'
down_revision: Union[str, None] = '37e18e3672ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.insert(Job)
        .values([
            {
                'id': '077c2e60-2a21-41c6-9b99-fce84d490a3a',
                'title': 'Junior',
                'salary': 30000,
                'days_to_promotion': datetime.timedelta(days=365)
            },
            {
                'id': 'acd00cd4-f548-4804-bbe2-31a72adebd78',
                'title': 'Middle',
                'salary': 80000,
                'days_to_promotion': datetime.timedelta(days=365*2)
            },
            {
                'id': '815b87e7-cc34-45dc-b520-38bc32372962',
                'title': 'Senior',
                'salary': 135000,
                'days_to_promotion': datetime.timedelta(days=1000)
            }
        ])
    )


def downgrade() -> None:
    op.execute(sa.delete(Job))

