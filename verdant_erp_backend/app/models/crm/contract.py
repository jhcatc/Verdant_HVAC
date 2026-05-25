from sqlalchemy import Column, String, ForeignKey, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base


class Contract(Base):

    __tablename__ = "crm_contracts"

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

    status = Column(String)
    sla_tier = Column(String)
    total_value = Column(Numeric)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    renewal_date = Column(DateTime)
    customer = relationship("Customer")