import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class ServiceOrderItem(Base):
    __tablename__ = "service_order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    order_id = Column(UUID(as_uuid=True), ForeignKey("service_orders.id"))

    name = Column(String, nullable=False)
    description = Column(String)

    is_completed = Column(Boolean, default=False)

    estimated_hours = Column(Float)
    actual_hours = Column(Float)

    order = relationship("ServiceOrder", back_populates="items")