import uuid
from sqlalchemy import (
    Column,
    String,
    Float,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class EquipmentMeasurement(Base):

    __tablename__ = "equipment_measurements"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    equipment_id = Column(
        UUID(as_uuid=True),
        ForeignKey("equipment.id", ondelete="CASCADE"),
        nullable=False
    )

    maintenance_log_id = Column(
        UUID(as_uuid=True),
        ForeignKey("maintenance_logs.id", ondelete="CASCADE"),
        nullable=False
    )

    measurement_type = Column(
        String,
        nullable=False
    )

    value = Column(Float)

    unit = Column(String)

    equipment = relationship(
        "Equipment",
        back_populates="measurements"
    )

    maintenance_log = relationship(
        "MaintenanceLog",
        back_populates="measurements"
    )