from sqlalchemy import (
    Column,
    Integer,
    String
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class EquipmentCategory(Base):

    __tablename__ = "equipment_categories"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String,
        unique=True,
        nullable=False
    )

    code = Column(
        String,
        unique=True,
        nullable=True
    )

    equipment_types = relationship(
        "EquipmentType",
        back_populates="category"
    )