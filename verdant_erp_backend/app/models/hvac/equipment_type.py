from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship
from app.core.database import Base

class EquipmentType(Base):

    __tablename__ = "equipment_types"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String,
        unique=True,
        nullable=False
    )

    category_id = Column(
        Integer,
        ForeignKey(
            'equipment_categories.id'
        ),
        nullable=False
    )

    category = relationship(
        'EquipmentCategory'
    )