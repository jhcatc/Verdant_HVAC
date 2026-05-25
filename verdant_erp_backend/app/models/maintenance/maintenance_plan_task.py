import uuid
from sqlalchemy import (
    Column,
    String,
    Text,
    Boolean,
    Integer,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class MaintenancePlanTask(Base):
    __tablename__ = "maintenance_plan_tasks"

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

    title = Column(String, nullable=False)

    description = Column(Text)

    estimated_minutes = Column(Integer, default=30)

    sort_order = Column(Integer, default=0)

    is_required = Column(Boolean, default=True)

    maintenance_plan = relationship(
        "MaintenancePlan",
        back_populates="tasks"
    )