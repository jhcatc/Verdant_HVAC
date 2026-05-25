import uuid
from sqlalchemy import Column, Float, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.core.database import Base


class AdjustmentRequest(Base):
    __tablename__ = "adjustment_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    item_id = Column(UUID(as_uuid=True))
    location_id = Column(UUID(as_uuid=True))

    quantity = Column(Float)
    reason = Column(String)

    requested_by = Column(UUID(as_uuid=True))
    approved_by = Column(UUID(as_uuid=True), nullable=True)

    status = Column(String, default="pending")  # pending | approved | rejected

    created_at = Column(DateTime, default=datetime.utcnow)