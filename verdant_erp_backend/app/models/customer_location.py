import uuid
from sqlalchemy import Column, String, ForeignKey, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class CustomerLocation(Base):
    __tablename__ = "customer_locations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(
        UUID(as_uuid=True),
        ForeignKey("customers.id"),
        nullable=False
    )
    name = Column(String, nullable=False)
    code = Column(String, nullable=True)
    location_type = Column(
        String,
        nullable=True
    )
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    zip_code = Column(String, nullable=True)
    country = Column(String, nullable=True)
    contact_name = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    customer = relationship(
        "Customer",
        back_populates="locations"
    )
    equipment = relationship(
        "Equipment",
        back_populates="location"
    )
    is_active = Column(
        Boolean,
        default=True
    )
    contact_email = Column(String, nullable=True)
    sla_tier = Column(String, nullable=True)
    access_notes = Column(Text, nullable=True)
    refrigerant_notes = Column(Text, nullable=True)
    technician_notes = Column(Text, nullable=True)