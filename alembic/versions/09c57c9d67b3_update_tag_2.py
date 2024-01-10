"""Update tag 2

Revision ID: 09c57c9d67b3
Revises: 1dae51f22bb2
Create Date: 2024-01-10 23:21:48.231448

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "09c57c9d67b3"
down_revision: Union[str, None] = "1dae51f22bb2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("tag", sa.Column("category", sa.String(), nullable=True))
    op.add_column("tag", sa.Column("color", sa.String(), nullable=False, server_default="grey"))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("tag", "color")
    op.drop_column("tag", "category")
    # ### end Alembic commands ###
