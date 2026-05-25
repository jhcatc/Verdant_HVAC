import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class Location(Base):
    __tablename__ = "locations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)  # "Main Warehouse", "Van 01"
    code = Column(String, unique=True)

    type = Column(String)  # warehouse | van
    is_active = Column(Boolean, default=True)