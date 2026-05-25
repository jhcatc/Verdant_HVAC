from sqlalchemy import Column, Integer, String
from app.core.database import Base


class PowerSource(Base):

    __tablename__ = "power_sources"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)