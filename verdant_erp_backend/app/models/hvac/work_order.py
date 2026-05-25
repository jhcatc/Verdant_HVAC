import uuid
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    DateTime,
    Text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class WorkOrder(Base):

    __tablename__ = "work_orders"

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

    technician_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True
    )

    status = Column(
        String,
        nullable=False,
        default="Pending"
    )

    priority = Column(
        String,
        nullable=False,
        default="Medium"
    )

    description = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    equipment = relationship(
        "Equipment",
        lazy="joined"
    )

    technician = relationship(
        "User",
        lazy="joined"
    )