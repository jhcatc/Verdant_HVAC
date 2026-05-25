import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Float,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from sqlalchemy.orm import relationship
from app.models.crm.proposal_totals import ProposalTotals
from sqlalchemy.orm import relationship


class Proposal(Base):

    __tablename__ = "crm_proposals"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    proposal_number = Column(
        String,
        nullable=False,
        unique=True,
        index=True
    )

    customer_id = Column(
        UUID(as_uuid=True),
        ForeignKey("customers.id"),
        nullable=False
    )

    # OPTIONAL
    # PIPELINE FLOW ONLY

    opportunity_id = Column(
        UUID(as_uuid=True),
        ForeignKey("crm_opportunities.id"),
        nullable=True
    )

    source_type = Column(
        String,
        nullable=False,
        default="DIRECT"
    )

    title = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        nullable=False,
        default="DRAFT"
    )

    amount = Column(
        Float,
        default=0
    )

    valid_until = Column(
        DateTime,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    line_items = relationship(
        "ProposalLineItem",
        back_populates="proposal",
        cascade="all, delete-orphan",
        order_by="ProposalLineItem.sort_order"
    )

    totals = relationship(
        "ProposalTotals",
        uselist=False,
        cascade="all, delete-orphan"
    )

    versions = relationship(
        "ProposalVersion",
        backref="proposal",
        cascade="all, delete-orphan",
        order_by="ProposalVersion.version_number"
    )