"""fix proposal line item uuid types

Revision ID: 62df8b8c90b9
Revises: ff8427f02e60
Create Date: 2026-05-24 20:32:11.961710

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '62df8b8c90b9'
down_revision: Union[str, Sequence[str], None] = 'ff8427f02e60'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():

    op.alter_column(
        'proposal_line_items',
        'id',
        existing_type=sa.VARCHAR(),
        type_=postgresql.UUID(as_uuid=True),
        postgresql_using='id::uuid'
    )

    op.alter_column(
        'proposal_line_items',
        'proposal_id',
        existing_type=sa.VARCHAR(),
        type_=postgresql.UUID(as_uuid=True),
        postgresql_using='proposal_id::uuid'
    )


def downgrade():

    op.alter_column(
        'proposal_line_items',
        'id',
        existing_type=postgresql.UUID(),
        type_=sa.VARCHAR()
    )

    op.alter_column(
        'proposal_line_items',
        'proposal_id',
        existing_type=postgresql.UUID(),
        type_=sa.VARCHAR()
    )