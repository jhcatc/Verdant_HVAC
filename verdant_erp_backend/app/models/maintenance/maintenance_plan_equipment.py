import uuid
from sqlalchemy import (
    Column,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
from sqlalchemy import UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy import DateTime, Boolean


class MaintenancePlanEquipment(Base):

    __tablename__ = "maintenance_plan_equipment"

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

    equipment_id = Column(
        UUID(as_uuid=True),
        ForeignKey("equipment.id"),
        nullable=False,
        index=True
    )

    """
    RELATIONSHIPS
    """

    maintenance_plan = relationship(
        "MaintenancePlan",
        back_populates="equipment"
    )

    equipment = relationship(
        "Equipment",
        back_populates="maintenance_plans",
        lazy="joined"
    )

    active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    __table_args__ = (
        UniqueConstraint(
            "maintenance_plan_id",
            "equipment_id",
            name="uq_pm_plan_equipment"
        ),
    )