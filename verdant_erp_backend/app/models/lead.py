import uuid

from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Integer,
    Float
)

from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class Lead(Base):

    __tablename__ = "crm_leads"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    title = Column(
        String,
        nullable=False
    )

    company = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        default="NEW"
    )

    estimated_value = Column(
        Float,
        default=0
    )

    probability = Column(
        Integer,
        default=0
    )

    source = Column(
        String,
        nullable=True
    )

    assigned_rep = Column(
        String,
        nullable=True
    )

    city = Column(
        String,
        nullable=True
    )

    email = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )