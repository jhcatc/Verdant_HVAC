import uuid
from datetime import datetime
from sqlalchemy import Column, Float, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class InventoryMovement(Base):
    __tablename__ = "inventory_movements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    item_id = Column(UUID(as_uuid=True), ForeignKey("inventory_items.id"))

    from_location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"), nullable=True)
    to_location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"), nullable=True)

    quantity = Column(Float)

    type = Column(String)  # in | out | transfer | adjustment

    reference = Column(String)  # order_id / adjustment_id
    performed_by = Column(UUID(as_uuid=True))  # 🔥 quién ejecuta

    created_at = Column(DateTime, default=datetime.utcnow)