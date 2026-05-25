from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Numeric,
    Integer,
    DateTime
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base


class Opportunity(Base):

    __tablename__ = "crm_opportunities"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    customer_id = Column(
        UUID(as_uuid=True),
        ForeignKey("customers.id"),
        nullable=False
    )

    title = Column(String, nullable=False)
    stage = Column(String)
    estimated_value = Column(Numeric)
    probability = Column(Integer)
    close_date = Column(DateTime)
    customer = relationship("Customer")