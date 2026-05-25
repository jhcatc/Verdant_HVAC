from sqlalchemy import (
    Column,
    String,
    Float,
    ForeignKey
)
from app.core.database import Base


class ProposalTotals(Base):

    __tablename__ = "proposal_totals"

    proposal_id = Column(
        String,
        ForeignKey(
            "crm_proposals.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )
    subtotal = Column(Float, default=0)
    discount_total = Column(Float, default=0)
    tax_total = Column(Float, default=0)
    grand_total = Column(Float, default=0)
    cost_total = Column(Float, default=0)
    margin_total = Column(Float, default=0)
    margin_percent = Column(Float, default=0)