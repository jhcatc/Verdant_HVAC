import uuid
from sqlalchemy import Column, String, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)
    sku = Column(String, unique=True, nullable=True)

    category = Column(String)  # material, tool, equipment, spare_part

    unit_cost = Column(Float)
    stock = Column(Float, default=0)

    is_active = Column(Boolean, default=True)
    min_stock = Column(Float, default=0)