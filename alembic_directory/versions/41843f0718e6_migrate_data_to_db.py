"""migrate data to db

Revision ID: 41843f0718e6
Revises: 74c1de072c3f
Create Date: 2024-06-12 13:37:58.660227

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '41843f0718e6'
down_revision: Union[str, None] = '74c1de072c3f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
