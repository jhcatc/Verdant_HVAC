from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.core.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    city = Column(String, nullable=True)  # ✅ FIX
    created_at = Column(DateTime, default=datetime.utcnow)  # ✅ FIX
    service_orders = relationship(
        "ServiceOrder",
        back_populates="customer",
    )
    locations = relationship(
        "CustomerLocation",
        back_populates="customer",
        cascade="all, delete-orphan"
    )
    contacts = relationship(
        "CustomerContact",
        cascade="all, delete-orphan"
    )
    addresses = relationship(
        "CustomerAddress",
        cascade="all, delete-orphan"
    )
    