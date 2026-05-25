"""inventory multi-location + adjustments

Revision ID: 8d26e4ad10a8
Revises: 86c4cb3075f4
Create Date: 2026-04-29 21:18:34.844242

"""
from typing import Sequence, Union
from sqlalchemy.dialects import postgresql
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d26e4ad10a8'
down_revision: Union[str, Sequence[str], None] = '86c4cb3075f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # =====================================================
    # 🔹 LOCATIONS
    # =====================================================
    op.create_table(
        'locations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('code', sa.String(), unique=True),
        sa.Column('type', sa.String()),  # warehouse | van
        sa.Column('is_active', sa.Boolean(), default=True)
    )

    # =====================================================
    # 🔹 INVENTORY STOCK (POR LOCATION)
    # =====================================================
    op.create_table(
        'inventory_stocks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('item_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('inventory_items.id')),
        sa.Column('location_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('locations.id')),
        sa.Column('quantity', sa.Float(), default=0)
    )

    # =====================================================
    # 🔹 ADJUSTMENT REQUESTS
    # =====================================================
    op.create_table(
        'adjustment_requests',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('item_id', postgresql.UUID(as_uuid=True)),
        sa.Column('location_id', postgresql.UUID(as_uuid=True)),
        sa.Column('quantity', sa.Float()),
        sa.Column('reason', sa.String()),
        sa.Column('requested_by', postgresql.UUID(as_uuid=True)),
        sa.Column('approved_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('status', sa.String(), default='pending'),
        sa.Column('created_at', sa.DateTime())
    )

    # =====================================================
    # 🔹 ALTER INVENTORY MOVEMENTS
    # =====================================================
    op.add_column('inventory_movements',
        sa.Column('from_location_id', postgresql.UUID(as_uuid=True), nullable=True)
    )

    op.add_column('inventory_movements',
        sa.Column('to_location_id', postgresql.UUID(as_uuid=True), nullable=True)
    )

    op.add_column('inventory_movements',
        sa.Column('performed_by', postgresql.UUID(as_uuid=True), nullable=True)
    )

    # FK constraints
    op.create_foreign_key(
        None,
        'inventory_movements',
        'locations',
        ['from_location_id'],
        ['id']
    )

    op.create_foreign_key(
        None,
        'inventory_movements',
        'locations',
        ['to_location_id'],
        ['id']
    )

def downgrade():

    op.drop_constraint(None, 'inventory_movements', type_='foreignkey')
    op.drop_constraint(None, 'inventory_movements', type_='foreignkey')

    op.drop_column('inventory_movements', 'performed_by')
    op.drop_column('inventory_movements', 'to_location_id')
    op.drop_column('inventory_movements', 'from_location_id')

    op.drop_table('adjustment_requests')
    op.drop_table('inventory_stocks')
    op.drop_table('locations')