"""create crm proposals

Revision ID: 49d0f584d32c
Revises: 6695779e5522
Create Date: 2026-05-23 22:20:48.755449
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '49d0f584d32c'
down_revision: Union[str, Sequence[str], None] = '6695779e5522'
branch_labels = None
depends_on = None


def upgrade() -> None:

    # =========================================================
    # CRM: EQUIPMENT BUNDLES
    # =========================================================
    op.create_table(
        'crm_equipment_bundles',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('base_price', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # =========================================================
    # PM: AGREEMENT TEMPLATES
    # =========================================================
    op.create_table(
        'pm_agreement_templates',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('billing_cycle', sa.String(), nullable=True),
        sa.Column('visits_per_year', sa.Integer(), nullable=True),
        sa.Column('base_price', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # =========================================================
    # CRM PROPOSALS
    # =========================================================
    op.create_table(
        'crm_proposals',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('proposal_number', sa.String(), nullable=False),
        sa.Column('customer_id', sa.UUID(), nullable=False),
        sa.Column('opportunity_id', sa.UUID(), nullable=True),
        sa.Column('source_type', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=True),
        sa.Column('valid_until', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id']),
        sa.ForeignKeyConstraint(['opportunity_id'], ['crm_opportunities.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(
        'ix_crm_proposals_proposal_number',
        'crm_proposals',
        ['proposal_number'],
        unique=True
    )

    # =========================================================
    # PROPOSAL ITEMS
    # =========================================================
    op.create_table(
        'crm_proposal_items',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('proposal_id', sa.UUID(), nullable=False),
        sa.Column('item_type', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=True),
        sa.Column('unit_price', sa.Float(), nullable=True),
        sa.Column('tax_rate', sa.Float(), nullable=True),
        sa.Column('total', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['proposal_id'], ['crm_proposals.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # =========================================================
    # FIX CRÍTICO: pm_schedules (UUID CONSISTENCY FIXED)
    # =========================================================

    op.create_table(
        'pm_schedules',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('equipment_id', sa.UUID(), nullable=False),

        # FIX
        sa.Column('maintenance_type_id', sa.Integer(), nullable=False),

        sa.Column('interval_days', sa.Integer(), nullable=False),
        sa.Column('next_due_date', sa.Date(), nullable=False),
        sa.Column('last_generated_at', sa.Date(), nullable=True),
        sa.Column('auto_generate_work_order', sa.Boolean(), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),

        sa.ForeignKeyConstraint(['equipment_id'], ['equipment.id']),
        sa.ForeignKeyConstraint(['maintenance_type_id'], ['maintenance_types.id']),

        sa.PrimaryKeyConstraint('id')
    )

    # =========================================================
    # EQUIPMENT BUNDLES IN PROPOSALS
    # =========================================================
    op.create_table(
        'proposal_equipment_bundles',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('proposal_id', sa.UUID(), nullable=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('total', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['proposal_id'], ['crm_proposals.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # =========================================================
    # LINE ITEMS (UI CORE)
    # =========================================================
    op.create_table(
        'proposal_line_items',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('proposal_id', sa.UUID(), nullable=False),
        sa.Column('item_type', sa.Enum(
            'equipment', 'labor', 'pm_plan', 'discount', 'misc',
            name='proposal_item_type'
        )),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('qty', sa.Integer(), nullable=True),
        sa.Column('unit_price', sa.Float(), nullable=True),
        sa.Column('tax_percent', sa.Float(), nullable=True),
        sa.Column('discount_percent', sa.Float(), nullable=True),
        sa.Column('total', sa.Float(), nullable=True),
        sa.Column('sort_order', sa.Integer(), nullable=True),
        sa.Column('is_optional', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['proposal_id'], ['crm_proposals.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # =========================================================
    # CONTRACTS CHANGES
    # =========================================================
    op.alter_column('crm_contracts', 'customer_id',
        existing_type=sa.UUID(),
        nullable=False
    )

    op.alter_column('crm_contracts', 'status',
        existing_type=sa.TEXT(),
        type_=sa.String()
    )

    op.alter_column('crm_contracts', 'sla_tier',
        existing_type=sa.TEXT(),
        type_=sa.String()
    )

    op.alter_column('crm_contracts', 'total_value',
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        type_=sa.Numeric()
    )

    op.alter_column('crm_contracts', 'start_date',
        existing_type=sa.TEXT(),
        type_=sa.DateTime()
    )

    op.alter_column('crm_contracts', 'end_date',
        existing_type=sa.TEXT(),
        type_=sa.DateTime()
    )

    op.alter_column('crm_contracts', 'renewal_date',
        existing_type=sa.TEXT(),
        type_=sa.DateTime()
    )

    op.drop_column('crm_contracts', 'opportunity_id')
    op.drop_column('crm_contracts', 'customer_name')
    op.drop_column('crm_contracts', 'version')
    op.drop_column('crm_contracts', 'created_at')

    # =========================================================
    # OPPORTUNITIES CLEANUP
    # =========================================================
    op.alter_column('crm_opportunities', 'customer_id',
        existing_type=sa.UUID(),
        nullable=False
    )

    op.alter_column('crm_opportunities', 'title',
        existing_type=sa.TEXT(),
        type_=sa.String()
    )

    op.alter_column('crm_opportunities', 'stage',
        existing_type=sa.TEXT(),
        type_=sa.String()
    )

    op.alter_column('crm_opportunities', 'estimated_value',
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        type_=sa.Numeric()
    )

    op.alter_column('crm_opportunities', 'close_date',
        existing_type=sa.TEXT(),
        type_=sa.DateTime()
    )

    op.drop_column('crm_opportunities', 'assigned_rep_name')
    op.drop_column('crm_opportunities', 'created_at')
    op.drop_column('crm_opportunities', 'sla_exposure')


def downgrade() -> None:
    op.drop_table('proposal_line_items')
    op.drop_table('proposal_equipment_bundles')
    op.drop_table('pm_schedules')
    op.drop_table('crm_proposal_items')
    op.drop_index('ix_crm_proposals_proposal_number', table_name='crm_proposals')
    op.drop_table('crm_proposals')
    op.drop_table('pm_agreement_templates')
    op.drop_table('crm_equipment_bundles')