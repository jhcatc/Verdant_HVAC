from sqlalchemy import Column, Integer, String
from app.core.database import Base


class EquipmentStatus(Base):

    __tablename__ = "equipment_statuses"

    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True, nullable=False)