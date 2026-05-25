from sqlalchemy import (
    Column,
    Float,
    String,
    Integer,
    ForeignKey,
    Enum,
    Boolean,
    Text
)
from sqlalchemy.orm import relationship
from app.core.database import Base
from sqlalchemy.dialects.postgresql import UUID


class ProposalLineItem(Base):

    __tablename__ = "proposal_line_items"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True
    )
    proposal_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "crm_proposals.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )
    item_type = Column(
        Enum(
            "equipment",
            "labor",
            "pm_plan",
            "discount",
            "misc",
            name="proposal_item_type"
        ),
        nullable=False
    )
    description = Column(Text)
    qty = Column(Float, default=1)
    unit_price = Column(Float, default=0)
    unit_cost = Column(Float, default=0)
    tax_percent = Column(Float, default=0)
    discount_percent = Column(Float, default=0)
    subtotal = Column(Float, default=0)
    discount_amount = Column(Float, default=0)
    taxable_amount = Column(Float, default=0)
    tax_amount = Column(Float, default=0)
    total = Column(Float, default=0)
    margin_amount = Column(Float, default=0)
    margin_percent = Column(Float, default=0)
    sort_order = Column(Integer, default=0)
    is_optional = Column(Boolean, default=False)
    proposal = relationship(
        "Proposal",
        back_populates="line_items"
    )