
from typing import Sequence, Union
from sqlalchemy.dialects import postgresql
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers

revision: str = 'ff8427f02e60'
down_revision: Union[str, Sequence[str], None] = '49d0f584d32c'
branch_labels = None
depends_on = None


proposal_item_type = postgresql.ENUM(
    'equipment',
    'labor',
    'pm_plan',
    'discount',
    'misc',
    name='proposal_item_type',
    create_type=False
)


def upgrade() -> None:

    # =====================================================
    # ENUM
    # =====================================================

    proposal_item_type.create(
        op.get_bind(),
        checkfirst=True
    )

    # =====================================================
    # PROPOSAL LINE ITEMS
    # =====================================================

    op.create_table(
        'proposal_line_items',

        sa.Column(
            'id',
            UUID(as_uuid=True),
            primary_key=True,
            nullable=False
        ),

        sa.Column(
            'proposal_id',
            UUID(as_uuid=True),
            sa.ForeignKey(
                'crm_proposals.id',
                ondelete='CASCADE'
            ),
            nullable=False
        ),

        sa.Column(
            'item_type',
            proposal_item_type,
            nullable=False
        ),

        sa.Column(
            'description',
            sa.Text(),
            nullable=True
        ),

        sa.Column(
            'qty',
            sa.Float(),
            nullable=False,
            server_default='1'
        ),

        sa.Column(
            'unit_price',
            sa.Float(),
            nullable=False,
            server_default='0'
        ),

        sa.Column(
            'unit_cost',
            sa.Float(),
            nullable=False,
            server_default='0'
        ),

        sa.Column(
            'tax_percent',
            sa.Float(),
            nullable=False,
            server_default='0'
        ),

        sa.Column(
            'discount_percent',
            sa.Float(),
            nullable=False,
            server_default='0'
        ),

        sa.Column(
            'subtotal',
            sa.Float(),
            nullable=False,
            server_default='0'
        ),

        sa.Column(
            'discount_amount',
            sa.Float(),
            nullable=False,
            server_default='0'
        ),

        sa.Column(
            'taxable_amount',
            sa.Float(),
            nullable=False,
            server_default='0'
        ),

        sa.Column(
            'tax_amount',
            sa.Float(),
            nullable=False,
            server_default='0'
        ),

        sa.Column(
            'total',
            sa.Float(),
            nullable=False,
            server_default='0'
        ),

        sa.Column(
            'margin_amount',
            sa.Float(),
            nullable=False,
            server_default='0'
        ),

        sa.Column(
            'margin_percent',
            sa.Float(),
            nullable=False,
            server_default='0'
        ),

        sa.Column(
            'sort_order',
            sa.Integer(),
            nullable=False,
            server_default='0'
        ),

        sa.Column(
            'is_optional',
            sa.Boolean(),
            nullable=False,
            server_default='false'
        )
    )

    op.create_index(
        'ix_proposal_line_items_proposal_id',
        'proposal_line_items',
        ['proposal_id']
    )

    # =====================================================
    # PROPOSAL TOTALS
    # =====================================================

    op.create_table(
        'proposal_totals',

        sa.Column(
            'proposal_id',
            UUID(as_uuid=True),
            sa.ForeignKey(
                'crm_proposals.id',
                ondelete='CASCADE'
            ),
            primary_key=True
        ),

        sa.Column(
            'subtotal',
            sa.Float(),
            nullable=False,
            server_default='0'
        ),

        sa.Column(
            'discount_total',
            sa.Float(),
            nullable=False,
            server_default='0'
        ),

        sa.Column(
            'tax_total',
            sa.Float(),
            nullable=False,
            server_default='0'
        ),

        sa.Column(
            'grand_total',
            sa.Float(),
            nullable=False,
            server_default='0'
        ),

        sa.Column(
            'cost_total',
            sa.Float(),
            nullable=False,
            server_default='0'
        ),

        sa.Column(
            'margin_total',
            sa.Float(),
            nullable=False,
            server_default='0'
        ),

        sa.Column(
            'margin_percent',
            sa.Float(),
            nullable=False,
            server_default='0'
        )
    )

    # =====================================================
    # PROPOSAL VERSIONS
    # =====================================================

    op.create_table(
        'proposal_versions',

        sa.Column(
            'id',
            UUID(as_uuid=True),
            primary_key=True,
            nullable=False
        ),

        sa.Column(
            'proposal_id',
            UUID(as_uuid=True),
            sa.ForeignKey(
                'crm_proposals.id',
                ondelete='CASCADE'
            ),
            nullable=False
        ),

        sa.Column(
            'version_number',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'subtotal',
            sa.Float(),
            nullable=False,
            server_default='0'
        ),

        sa.Column(
            'taxes',
            sa.Float(),
            nullable=False,
            server_default='0'
        ),

        sa.Column(
            'discounts',
            sa.Float(),
            nullable=False,
            server_default='0'
        ),

        sa.Column(
            'total',
            sa.Float(),
            nullable=False,
            server_default='0'
        ),

        sa.Column(
            'margin',
            sa.Float(),
            nullable=False,
            server_default='0'
        ),

        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False
        )
    )


def downgrade() -> None:

    op.drop_table('proposal_versions')

    op.drop_table('proposal_totals')

    op.drop_index(
        'ix_proposal_line_items_proposal_id',
        table_name='proposal_line_items'
    )

    op.drop_table('proposal_line_items')

    proposal_item_type.drop(
        op.get_bind(),
        checkfirst=True
    )