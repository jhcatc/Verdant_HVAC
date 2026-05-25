from sqlalchemy import Column, Integer, String
from app.core.database import Base


class VoltageType(Base):

    __tablename__ = "voltage_types"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)