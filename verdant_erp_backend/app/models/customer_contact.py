from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base
from sqlalchemy.orm import relationship

class CustomerContact(Base):
    __tablename__ = "customer_contacts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"))
    name = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)
    role = Column(String)  # manager, billing, etc
 
    customer = relationship(
        "Customer",
        back_populates="contacts"
    )