"""requests.updated_at, requests.query unique

Revision ID: c226e3e633d2
Revises: 4c678e8f5275
Create Date: 2024-10-21 17:09:37.608207

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c226e3e633d2'
down_revision: Union[str, None] = '4c678e8f5275'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('requests', sa.Column('updated_at', sa.Date(), server_default=sa.text('now()'), nullable=False))
    op.create_unique_constraint(None, 'requests', ['query'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'requests', type_='unique')
    op.drop_column('requests', 'updated_at')
    # ### end Alembic commands ###
