from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base
from sqlalchemy.orm import relationship

class CustomerAddress(Base):
    __tablename__ = "customer_addresses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"))
    label = Column(String)  # HQ, Branch, etc
    address = Column(String)
    city = Column(String)

    customer = relationship(
        "Customer",
        back_populates="addresses"
    )