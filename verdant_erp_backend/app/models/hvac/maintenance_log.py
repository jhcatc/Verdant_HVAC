import uuid

from sqlalchemy import (
    Column,
    String,
    Text,
    ForeignKey,
    DateTime
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class MaintenanceLog(Base):
    __tablename__ = "maintenance_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    equipment_id = Column(
        UUID(as_uuid=True),
        ForeignKey("equipment.id", ondelete="CASCADE"),
        nullable=False
    )

    technician_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    maintenance_type_id = Column(
        ForeignKey("maintenance_types.id"),
        nullable=False
    )

    notes = Column(Text)

    equipment_condition = Column(String)

    refrigerant_added = Column(String)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    equipment = relationship(
        "Equipment",
        back_populates="maintenance_logs"
    )

    technician = relationship(
        "User"
    )

    maintenance_type = relationship(
        "MaintenanceType"
    )

    measurements = relationship(
        "EquipmentMeasurement",
        back_populates="maintenance_log",
        cascade="all, delete-orphan"
    )

    photos = relationship(
        "EquipmentPhoto",
        back_populates="maintenance_log",
        cascade="all, delete-orphan"
    )

    documents = relationship(
        "EquipmentDocument",
        back_populates="maintenance_log",
        cascade="all, delete-orphan"
    )

    components = relationship(
        "EquipmentComponent",
        back_populates="maintenance_log"
    )