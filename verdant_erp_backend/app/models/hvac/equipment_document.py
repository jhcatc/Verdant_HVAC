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

class EquipmentDocument(Base):

    __tablename__ = "equipment_documents"

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
        nullable=True
    )

    file_name = Column(
        String(255),
        nullable=False
    )

    file_path = Column(
        Text,
        nullable=False
    )

    document_type = Column(
        String(100),
        nullable=True
    )

    uploaded_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    equipment = relationship(
        "Equipment",
        back_populates="documents"
    )

    maintenance_log = relationship(
        "MaintenanceLog",
        back_populates="documents"
    )