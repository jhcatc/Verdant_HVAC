"""proposal phase 2b

Revision ID: 708db46c46ab
Revises: 62df8b8c90b9
Create Date: 2026-05-24 21:52:50.336346
"""

from typing import Sequence, Union
from uuid import uuid4

from alembic import op

import sqlalchemy as sa

from sqlalchemy.dialects import postgresql


# revision identifiers
revision: str = '708db46c46ab'

down_revision: Union[
    str,
    Sequence[str],
    None
] = '62df8b8c90b9'

branch_labels: Union[
    str,
    Sequence[str],
    None
] = None

depends_on: Union[
    str,
    Sequence[str],
    None
] = None


# =====================================================
# UPGRADE
# =====================================================

def upgrade() -> None:

    # =================================================
    # PROPOSAL VERSIONS
    # =================================================

    op.add_column(

        'proposal_versions',

        sa.Column(
            'status',
            sa.String(),
            nullable=True
        )
    )

    op.add_column(

        'proposal_versions',

        sa.Column(
            'snapshot',
            sa.JSON(),
            nullable=True
        )
    )

    op.add_column(

        'proposal_versions',

        sa.Column(
            'pdf_url',
            sa.Text(),
            nullable=True
        )
    )

    op.add_column(

        'proposal_versions',

        sa.Column(
            'approved_by',
            sa.String(),
            nullable=True
        )
    )

    op.add_column(

        'proposal_versions',

        sa.Column(
            'approved_at',
            sa.DateTime(timezone=True),
            nullable=True
        )
    )

    op.add_column(

        'proposal_versions',

        sa.Column(
            'customer_accepted_at',
            sa.DateTime(timezone=True),
            nullable=True
        )
    )

    # =================================================
    # CRM EQUIPMENT BUNDLES
    # =================================================

    op.create_table(

        'crm_equipment_bundles',

        sa.Column(
            'id',
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            default=uuid4
        ),

        sa.Column(
            'name',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'description',
            sa.Text(),
            nullable=True
        ),

        sa.Column(
            'base_price',
            sa.Float(),
            nullable=True
        )
    )

    # =================================================
    # PROPOSAL EQUIPMENT BUNDLES
    # =================================================

    op.create_table(

        'proposal_equipment_bundles',

        sa.Column(
            'id',
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            default=uuid4
        ),

        sa.Column(
            'proposal_id',
            postgresql.UUID(as_uuid=True),
            nullable=False
        ),

        sa.Column(
            'name',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'description',
            sa.Text(),
            nullable=True
        ),

        sa.Column(
            'total',
            sa.Float(),
            nullable=True
        ),

        sa.ForeignKeyConstraint(
            ['proposal_id'],
            ['crm_proposals.id'],
            ondelete='CASCADE'
        )
    )

    # =================================================
    # PM AGREEMENT TEMPLATES
    # =================================================

    op.create_table(

        'pm_agreement_templates',

        sa.Column(
            'id',
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            default=uuid4
        ),

        sa.Column(
            'name',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'description',
            sa.Text(),
            nullable=True
        ),

        sa.Column(
            'billing_cycle',
            sa.String(),
            nullable=True
        ),

        sa.Column(
            'visits_per_year',
            sa.Integer(),
            nullable=True
        ),

        sa.Column(
            'base_price',
            sa.Float(),
            nullable=True
        )
    )


# =====================================================
# DOWNGRADE
# =====================================================

def downgrade() -> None:

    # =================================================
    # DROP TABLES
    # =================================================

    op.drop_table(
        'pm_agreement_templates'
    )

    op.drop_table(
        'proposal_equipment_bundles'
    )

    op.drop_table(
        'crm_equipment_bundles'
    )

    # =================================================
    # REMOVE VERSION COLUMNS
    # =================================================

    op.drop_column(
        'proposal_versions',
        'customer_accepted_at'
    )

    op.drop_column(
        'proposal_versions',
        'approved_at'
    )

    op.drop_column(
        'proposal_versions',
        'approved_by'
    )

    op.drop_column(
        'proposal_versions',
        'pdf_url'
    )

    op.drop_column(
        'proposal_versions',
        'snapshot'
    )

    op.drop_column(
        'proposal_versions',
        'status'
    )