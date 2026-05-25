"""proposal engine phase 2b

Revision ID: 00ab78d3913f
Revises: 708db46c46ab
Create Date: 2026-05-24 22:50:26.637854

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa



revision = '00ab78d3913f'
down_revision = '708db46c46ab'
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(

        'equipment_catalog',

        sa.Column(
            'id',
            sa.String(),
            primary_key=True
        ),

        sa.Column(
            'sku',
            sa.String(),
            unique=True
        ),

        sa.Column(
            'manufacturer',
            sa.String()
        ),

        sa.Column(
            'model_number',
            sa.String()
        ),

        sa.Column(
            'name',
            sa.String()
        ),

        sa.Column(
            'category',
            sa.String()
        ),

        sa.Column(
            'cooling_capacity',
            sa.Float()
        ),

        sa.Column(
            'heating_capacity',
            sa.Float()
        ),

        sa.Column(
            'equipment_cost',
            sa.Float()
        ),

        sa.Column(
            'equipment_price',
            sa.Float()
        ),

        sa.Column(
            'is_active',
            sa.Boolean(),
            nullable=False,
            server_default=sa.true()
        )
    )


def downgrade():

    op.drop_table(
        'equipment_catalog'
    )