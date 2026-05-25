"""preventive_maintenance_engine

Revision ID: a9d5dcdaf4a3
Revises: e404b3234151
Create Date: 2026-05-14 20:32:44.914129
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = 'a9d5dcdaf4a3'
down_revision: Union[str, Sequence[str], None] = 'e404b3234151'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# =========================================================
# ENUMS
# =========================================================

service_order_priority_enum = sa.Enum(
    'low',
    'medium',
    'high',
    'urgent',
    name='service_order_priority'
)


def upgrade() -> None:

    """
    CREATE ENUM FIRST
    """

    service_order_priority_enum.create(
        op.get_bind(),
        checkfirst=True
    )

    """
    ADD COLUMN
    """

    op.add_column(
        'service_orders',

        sa.Column(
            'priority',

            service_order_priority_enum,

            nullable=False,

            server_default='medium'
        )
    )

    """
    REMOVE SERVER DEFAULT
    """

    op.alter_column(
        'service_orders',
        'priority',
        server_default=None
    )


def downgrade() -> None:

    op.drop_column(
        'service_orders',
        'priority'
    )

    service_order_priority_enum.drop(
        op.get_bind(),
        checkfirst=True
    )