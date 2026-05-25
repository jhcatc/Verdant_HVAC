import uuid
from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class ProposalItem(Base):

    __tablename__ = "crm_proposal_items"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    proposal_id = Column(
        UUID(as_uuid=True),
        ForeignKey("crm_proposals.id"),
        nullable=False
    )

    item_type = Column(
        String,
        nullable=False
    )
    # EQUIPMENT
    # LABOR
    # PM_PLAN
    # DISCOUNT

    description = Column(
        String,
        nullable=False
    )

    quantity = Column(
        Integer,
        default=1
    )

    unit_price = Column(
        Float,
        default=0
    )

    tax_rate = Column(
        Float,
        default=0
    )

    total = Column(
        Float,
        default=0
    )