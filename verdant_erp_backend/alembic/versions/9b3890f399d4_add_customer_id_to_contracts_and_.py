"""add customer_id to crm contracts and crm opportunities

Revision ID: 9b3890f399d4
Revises: 9f6ee21f75f9
Create Date: 2026-05-22

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "9b3890f399d4"
down_revision: Union[str, Sequence[str], None] = "9f6ee21f75f9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # =====================================================
    # CRM CONTRACTS
    # =====================================================

    op.add_column(
        "crm_contracts",
        sa.Column(
            "customer_id",
            postgresql.UUID(as_uuid=True),
            nullable=True,
        ),
    )

    op.create_foreign_key(
        "fk_crm_contracts_customer_id",
        "crm_contracts",
        "customers",
        ["customer_id"],
        ["id"],
    )

    # =====================================================
    # CRM OPPORTUNITIES
    # =====================================================

    op.add_column(
        "crm_opportunities",
        sa.Column(
            "customer_id",
            postgresql.UUID(as_uuid=True),
            nullable=True,
        ),
    )

    op.create_foreign_key(
        "fk_crm_opportunities_customer_id",
        "crm_opportunities",
        "customers",
        ["customer_id"],
        ["id"],
    )


def downgrade() -> None:

    # =====================================================
    # CRM OPPORTUNITIES
    # =====================================================

    op.drop_constraint(
        "fk_crm_opportunities_customer_id",
        "crm_opportunities",
        type_="foreignkey",
    )

    op.drop_column(
        "crm_opportunities",
        "customer_id",
    )

    # =====================================================
    # CRM CONTRACTS
    # =====================================================

    op.drop_constraint(
        "fk_crm_contracts_customer_id",
        "crm_contracts",
        type_="foreignkey",
    )

    op.drop_column(
        "crm_contracts",
        "customer_id",
    )