import uuid
from sqlalchemy import Column, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.core.database import Base


class EquipmentTelemetry(Base):
    __tablename__ = "equipment_telemetry"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    equipment_id = Column(UUID(as_uuid=True), nullable=False, index=True)

    temperature = Column(Float, nullable=True)
    pressure = Column(Float, nullable=True)
    energy_kw = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)