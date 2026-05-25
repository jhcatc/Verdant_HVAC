import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class ServiceOrderTask(Base):
    __tablename__ = "service_order_tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    order_id = Column(UUID(as_uuid=True), ForeignKey("service_orders.id"))

    title = Column(String, nullable=False)
    description = Column(String)
    is_done = Column(Boolean, default=False)

    # 🔥 ESTA LÍNEA DEBE COINCIDIR EXACTO
    order = relationship("ServiceOrder", back_populates="tasks")