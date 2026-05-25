import uuid
from sqlalchemy import Column, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class InventoryStock(Base):
    __tablename__ = "inventory_stocks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    item_id = Column(UUID(as_uuid=True), ForeignKey("inventory_items.id"))
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"))

    quantity = Column(Float, default=0)