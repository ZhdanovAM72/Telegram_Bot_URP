"""Added full_name

Revision ID: d9b798c42ecb
Revises: 8c45e0cb3c27
Create Date: 2024-06-07 09:28:22.725771

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9b798c42ecb'
down_revision: Union[str, None] = '8c45e0cb3c27'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('full_name', sa.String(length=64), nullable=False))
    op.create_unique_constraint(None, 'users', ['id'])
    op.create_unique_constraint(None, 'users', ['full_name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'full_name')
    # ### end Alembic commands ###