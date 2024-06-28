"""db state

Revision ID: 6fc578f728f0
Revises: 5d858bdac739
Create Date: 2024-06-28 22:55:53.993054

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6fc578f728f0'
down_revision: Union[str, None] = '5d858bdac739'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('testing',
    sa.Column('testid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['testid'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('testid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('testing')
    # ### end Alembic commands ###