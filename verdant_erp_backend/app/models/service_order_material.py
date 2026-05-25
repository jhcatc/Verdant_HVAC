import uuid
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class ServiceOrderMaterial(Base):
    __tablename__ = "service_order_materials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    order_id = Column(UUID(as_uuid=True), ForeignKey("service_orders.id"))
    inventory_item_id = Column(UUID(as_uuid=True), ForeignKey("inventory_items.id"))

    name = Column(String)
    unit_cost = Column(Float)
    quantity = Column(Float)

    order = relationship("ServiceOrder", back_populates="materials")
    item = relationship("InventoryItem")