from sqlalchemy import (
    Column,
    Integer,
    String
)

from app.core.database import Base


class WorkOrderSource(Base):

    __tablename__ = "work_order_sources"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String,
        nullable=False,
        unique=True
    )