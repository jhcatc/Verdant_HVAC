"""add equipment_id to equipment components

Revision ID: cb0607407bb7
Revises: e62732457b66
Create Date: 2026-05-09 20:43:11.441960
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'cb0607407bb7'
down_revision: Union[str, Sequence[str], None] = 'e62732457b66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        'equipment_components',

        sa.Column(
            'id',
            sa.UUID(),
            nullable=False
        ),

        sa.Column(
            'equipment_id',
            sa.UUID(),
            nullable=False
        ),

        sa.Column(
            'name',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'brand',
            sa.String(),
            nullable=True
        ),

        sa.Column(
            'model',
            sa.String(),
            nullable=True
        ),

        sa.Column(
            'serial_number',
            sa.String(),
            nullable=True
        ),

        sa.Column(
            'status',
            sa.String(),
            nullable=True
        ),

        sa.Column(
            'notes',
            sa.Text(),
            nullable=True
        ),

        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=True
        ),

        sa.ForeignKeyConstraint(
            ['equipment_id'],
            ['equipment.id'],
            ondelete='CASCADE'
        ),

        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:

    op.drop_table('equipment_components')