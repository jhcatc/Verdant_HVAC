from sqlalchemy import (
    Column,
    String,
    Float,
    Boolean
)
from app.core.database import Base


class EquipmentCatalog(Base):
    __tablename__ = "equipment_catalog"
    id = Column(String, primary_key=True)
    sku = Column(String, unique=True)
    manufacturer = Column(String)
    model_number = Column(String)
    name = Column(String)
    category = Column(String)
    cooling_capacity = Column(Float)
    heating_capacity = Column(Float)
    equipment_cost = Column(Float)
    equipment_price = Column(Float)
    is_active = Column(Boolean, default=True)