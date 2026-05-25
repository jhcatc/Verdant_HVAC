from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    Date,
    Boolean,
    Text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base

class PMSchedule(Base):

    __tablename__ = "pm_schedules"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    equipment_id = Column(
        UUID(as_uuid=True),
        ForeignKey("equipment.id"),
        nullable=False
    )

    maintenance_type_id = Column(
        UUID(as_uuid=True),
        ForeignKey("maintenance_types.id"),
        nullable=False
    )

    interval_days = Column(
        Integer,
        nullable=False
    )

    next_due_date = Column(
        Date,
        nullable=False
    )

    last_generated_at = Column(
        Date,
        nullable=True
    )

    auto_generate_work_order = Column(
        Boolean,
        default=True
    )

    active = Column(
        Boolean,
        default=True
    )

    notes = Column(
        Text,
        nullable=True
    )

    equipment = relationship("Equipment")

    maintenance_type = relationship(
        "MaintenanceType"
    )