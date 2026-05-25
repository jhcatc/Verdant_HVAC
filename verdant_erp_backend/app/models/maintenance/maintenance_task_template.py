import uuid

from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    ForeignKey,
    Text
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship

from app.core.database import Base


class MaintenanceTaskTemplate(Base):

    __tablename__ = "maintenance_task_templates"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    maintenance_plan_id = Column(
        UUID(as_uuid=True),
        ForeignKey("maintenance_plans.id"),
        nullable=False,
        index=True
    )

    title = Column(
        String,
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    sort_order = Column(
        Integer,
        default=0
    )

    estimated_minutes = Column(
        Integer,
        nullable=True
    )

    is_required = Column(
        Boolean,
        default=True
    )

    requires_photo = Column(
        Boolean,
        default=False
    )

    requires_measurement = Column(
        Boolean,
        default=False
    )

    requires_pass_fail = Column(
        Boolean,
        default=False
    )

    measurement_unit = Column(
        String,
        nullable=True
    )

    maintenance_plan = relationship(
        "MaintenancePlan",
        back_populates="task_templates"
    )