from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'a1ed6173d393'
down_revision = 'a9d5dcdaf4a3'
branch_labels = None
depends_on = None


def upgrade():

    op.add_column(
        'maintenance_plans',
        sa.Column(
            'end_date',
            sa.Date(),
            nullable=True
        )
    )


def downgrade():

    op.drop_column(
        'maintenance_plans',
        'end_date'
    )