"""Create superuser admin (password: admin)

Revision ID: 956514f1c056
Revises: 3d8dfa8405d9
Create Date: 2024-04-27 12:54:18.388441

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from auth.models import User
from auth.utils import hash_password


# revision identifiers, used by Alembic.
revision: str = '956514f1c056'
down_revision: Union[str, None] = '3d8dfa8405d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.insert(User)
        .values(
            id='33755f68-4737-4de7-bd09-f589fb458b9e',
            username='admin',
            password=hash_password('admin'),
            first_name='Admin',
            last_name='Admin',
            is_superuser=True,
            is_staff=False
        )
    )


def downgrade() -> None:
    op.execute(
        sa.delete(User)
        .where(User.id == '33755f68-4737-4de7-bd09-f589fb458b9e')
    )

