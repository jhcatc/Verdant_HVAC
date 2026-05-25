import uuid
from sqlalchemy import Column, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class ServiceOrderAssignment(Base):
    __tablename__ = "service_order_assignments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    order_id = Column(UUID(as_uuid=True), ForeignKey("service_orders.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    is_primary = Column(Boolean, default=False)

    assigned_at = Column(DateTime, default=datetime.utcnow)

    order = relationship("ServiceOrder", back_populates="assignments")
    user = relationship("User")