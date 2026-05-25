import uuid
import enum
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Text,
    Enum,
    Float,
    Boolean
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
from app.models.customer import Customer
from pydantic import BaseModel


class WorkOrderSource(str, enum.Enum):
    manual = "manual"
    preventive_maintenance = "preventive_maintenance"
    inspection = "inspection"
    predictive = "predictive"
    emergency = "emergency"

class ServiceOrderStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING = "pending"
    READY_FOR_DISPATCH = "ready_for_dispatch"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ServiceOrderPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class ServiceOrder(Base):
    __tablename__ = "service_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # 🧾 INFO
    code = Column(String, unique=True, index=True)  # SO-0001
    title = Column(String, nullable=False)
    description = Column(Text)

    source = Column(
        Enum(
            WorkOrderSource,
            name="work_order_source",
            values_callable=lambda x: [e.value for e in x]
        ),
        nullable=False,
        default=WorkOrderSource.manual
    )

    status = Column(
        Enum(
            ServiceOrderStatus,
            name="service_order_status",
            values_callable=lambda x: [e.value for e in x]  # 🔥 CLAVE
        ),
        nullable=False,
        default=ServiceOrderStatus.PENDING
    )

    priority = Column(
        Enum(
            ServiceOrderPriority,
            name="service_order_priority",
            values_callable=lambda x: [e.value for e in x]
        ),
        nullable=False,
        default=ServiceOrderPriority.medium
    )

    PRIORITY_MAP = {
        "low": 1,
        "medium": 2,
        "high": 3,
        "urgent": 4
    }

    is_active = Column(Boolean, default=True)

    # 👤 CLIENTE
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)

    customer_location_id = Column(
        UUID(as_uuid=True),
        ForeignKey("customer_locations.id"),
        nullable=True,
        index=True
    )

    equipment_id = Column(
        UUID(as_uuid=True),
        ForeignKey("equipment.id"),
        nullable=True,
        index=True
    )

    maintenance_plan_id = Column(
        UUID(as_uuid=True),
        ForeignKey("maintenance_plans.id"),
        nullable=True,
        index=True
    )

    # 📍 UBICACIÓN
    address = Column(String)
    city = Column(String, nullable=True)
    latitude = Column(Float)
    longitude = Column(Float)

    # ⏱️ PLANIFICACIÓN
    scheduled_at = Column(DateTime)
    duration_hours = Column(Float, default=1)
    sla_deadline = Column(DateTime)

    # ⏱️ EJECUCIÓN REAL
    started_at = Column(DateTime)
    completed_at = Column(DateTime)

    # 💰 COSTOS
    estimated_material_cost = Column(Float, default=0)
    estimated_labor_cost = Column(Float, default=0)
    labor_cost = Column(Float, default=0)
    actual_material_cost = Column(Float, default=0)
    actual_labor_cost = Column(Float, default=0)

    estimated_cost = Column(Float, default=0)  # total estimado
    actual_cost = Column(Float, default=0)     # total real

    # 🧾 CONTROL
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

   
    # 🔗 RELACIONES
    customer = relationship("Customer", back_populates="service_orders")

    customer_location = relationship(
        "CustomerLocation",
        lazy="joined"
    )

    equipment = relationship(
        "Equipment",
        lazy="joined"
    )

    maintenance_plan = relationship(
        "MaintenancePlan",
        lazy="joined"
    )

    assignments = relationship("ServiceOrderAssignment", back_populates="order")
    materials = relationship("ServiceOrderMaterial", back_populates="order")
    logs = relationship(
    "ServiceOrderLog",
    back_populates="order",
    cascade="all, delete-orphan")
    items = relationship(
        "ServiceOrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )
    tasks = relationship(
        "ServiceOrderTask",
        back_populates="order",
        cascade="all, delete-orphan"
    )

class ServiceOrderOut(BaseModel):
    id: str
    status: str

    class Config:
        use_enum_values = True  # 🔥 ESTO ES CLAVE