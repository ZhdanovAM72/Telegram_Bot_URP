"""merge heads

Revision ID: 5e9e9cd0cd55
Revises: dd6b5fd42595, 54f16321fdbb
Create Date: 2024-05-31 11:07:42.340401

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e9e9cd0cd55'
down_revision: Union[str, None] = ('dd6b5fd42595', '54f16321fdbb')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
