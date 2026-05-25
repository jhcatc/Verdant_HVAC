# app/models/maintenance/maintenance_plan.py

import uuid
import enum
from sqlalchemy import Boolean
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    Date,
    Boolean,
    Text,
    Enum,
    DateTime
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class MaintenancePlanType(str, enum.Enum):
    preventive = "preventive"
    inspection = "inspection"
    predictive = "predictive"


class MaintenancePlan(Base):

    __tablename__ = "maintenance_plans"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    company_id = Column(
        UUID(as_uuid=True),
        nullable=True
    )

    customer_id = Column(
        UUID(as_uuid=True),
        ForeignKey("customers.id"),
        nullable=False,
        index=True
    )

    location_id = Column(
        UUID(as_uuid=True),
        ForeignKey("customer_locations.id"),
        nullable=False,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    """
    SCHEDULING
    """

    frequency_days = Column(
        Integer,
        nullable=False
    )

    start_date = Column(
        Date,
        nullable=False
    )

    end_date = Column(
        Date,
        nullable=True
    )

    next_run_date = Column(
        Date,
        nullable=True,
        index=True
    )

    last_run_date = Column(
        Date,
        nullable=True
    )

    is_recurring = Column(
        Boolean,
        default=True
    )

    """
    AUTOMATION
    """

    auto_generate_work_orders = Column(
        Boolean,
        default=True
    )

    generate_per_equipment = Column(
        Boolean,
        default=True
    )

    """
    STATUS
    """

    active = Column(
        Boolean,
        default=True,
        index=True
    )

    """
    PLAN TYPE
    """

    plan_type = Column(
        Enum(
            MaintenancePlanType,
            name="maintenance_plan_type",
            values_callable=lambda x: [e.value for e in x]
        ),
        nullable=False,
        default=MaintenancePlanType.preventive
    )

    """
    AUDIT
    """

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )

    """
    RELATIONSHIPS
    """

    customer = relationship(
        "Customer",
        lazy="joined"
    )

    location = relationship(
        "CustomerLocation",
        lazy="joined"
    )

    equipment = relationship(
        "MaintenancePlanEquipment",
        back_populates="maintenance_plan",
        cascade="all, delete-orphan"
    )

    task_templates = relationship(
        "MaintenanceTaskTemplate",
        back_populates="maintenance_plan",
        cascade="all, delete-orphan"
    )

    last_generated_at = Column(DateTime, nullable=True)

    is_active = Column(Boolean, default=True)

    tasks = relationship(
        "MaintenancePlanTask",
        back_populates="maintenance_plan",
        cascade="all, delete-orphan"
    )