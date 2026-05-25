"""add duration_hours to service_orders

Revision ID: aa70ab3a14dd
Revises: f74909f236e3
Create Date: 2026-05-03 19:52:31.162705

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa70ab3a14dd'
down_revision: Union[str, Sequence[str], None] = 'f74909f236e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        'service_orders',
        sa.Column('duration_hours', sa.Float(), nullable=True, server_default='1')
    )

def downgrade():
    op.drop_column('service_orders', 'duration_hours')
