import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class ServiceOrderLog(Base):
    __tablename__ = "service_order_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    order_id = Column(UUID(as_uuid=True), ForeignKey("service_orders.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    action = Column(String)  # created, updated, assigned, completed
    description = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    order = relationship("ServiceOrder", back_populates="logs")
    user = relationship("User")