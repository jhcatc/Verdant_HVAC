from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Brand(Base):

    __tablename__ = "equipment_brands"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String(120),
        nullable=False
    )