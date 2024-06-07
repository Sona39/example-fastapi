"""add content column

Revision ID: 734cc1af0b0b
Revises: 0aec88395af0
Create Date: 2024-06-07 13:09:52.421016

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '734cc1af0b0b'
down_revision: Union[str, None] = '0aec88395af0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
