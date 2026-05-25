from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    Float,
    DateTime,
    JSON,
    Text
)
from sqlalchemy.sql import func
from app.core.database import Base


class ProposalVersion(Base):

    __tablename__ = "proposal_versions"

    id = Column(String, primary_key=True)
    proposal_id = Column(
        String,
        ForeignKey("crm_proposals.id")
    )
    version_number = Column(Integer)
    status = Column(
        String,
        default="DRAFT"
    )
    snapshot = Column(JSON)
    subtotal = Column(Float, default=0)
    taxes = Column(Float, default=0)
    discounts = Column(Float, default=0)
    total = Column(Float, default=0)
    margin = Column(Float, default=0)
    pdf_url = Column(Text, nullable=True)
    approved_by = Column(
        String,
        nullable=True
    )
    approved_at = Column(
        DateTime(timezone=True),
        nullable=True
    )
    customer_accepted_at = Column(
        DateTime(timezone=True),
        nullable=True
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )