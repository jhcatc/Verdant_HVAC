"""create crm leads table

Revision ID: 6695779e5522
Revises: 9b3890f399d4
Create Date: 2026-05-23 14:07:08.447204
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6695779e5522"
down_revision: Union[str, Sequence[str], None] = "9b3890f399d4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "crm_leads",

        sa.Column(
            "id",
            sa.UUID(),
            nullable=False
        ),

        sa.Column(
            "title",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "company",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "status",
            sa.String(),
            nullable=True
        ),

        sa.Column(
            "estimated_value",
            sa.Float(),
            nullable=True
        ),

        sa.Column(
            "probability",
            sa.Integer(),
            nullable=True
        ),

        sa.Column(
            "source",
            sa.String(),
            nullable=True
        ),

        sa.Column(
            "assigned_rep",
            sa.String(),
            nullable=True
        ),

        sa.Column(
            "city",
            sa.String(),
            nullable=True
        ),

        sa.Column(
            "email",
            sa.String(),
            nullable=True
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=True
        ),

        sa.PrimaryKeyConstraint("id")
    )


def downgrade() -> None:

    op.drop_table("crm_leads")