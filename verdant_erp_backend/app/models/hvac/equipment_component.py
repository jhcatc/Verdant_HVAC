import uuid
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Date,
    DateTime,
    Text,
    Boolean
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class EquipmentComponent(Base):

    __tablename__ = "equipment_components"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    equipment_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "equipment.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    maintenance_log_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "maintenance_logs.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )

    component_type = Column(
        String(100),
        nullable=False
    )

    component_name = Column(
        String(255),
        nullable=False
    )

    manufacturer = Column(
        String(255),
        nullable=True
    )

    model_number = Column(
        String(255),
        nullable=True
    )

    serial_number = Column(
        String(255),
        nullable=True
    )

    status = Column(
        String(50),
        nullable=False,
        default="active"
    )

    installation_date = Column(
        Date,
        nullable=True
    )

    replacement_date = Column(
        Date,
        nullable=True
    )

    warranty_expiration = Column(
        Date,
        nullable=True
    )

    useful_life_months = Column(
        String(50),
        nullable=True
    )

    failure_reason = Column(
        Text,
        nullable=True
    )

    replacement_reason = Column(
        Text,
        nullable=True
    )

    notes = Column(
        Text,
        nullable=True
    )

    is_critical = Column(
        Boolean,
        nullable=False,
        default=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    equipment = relationship(
        "Equipment",
        back_populates="components"
    )

    maintenance_log = relationship(
        "MaintenanceLog",
        back_populates="components"
    )