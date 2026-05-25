import uuid
from sqlalchemy import (
    Column,
    String,
    Float,
    Text
)
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class EquipmentBundle(Base):

    __tablename__ = "crm_equipment_bundles"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name = Column(
        String,
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    base_price = Column(
        Float,
        default=0
    )