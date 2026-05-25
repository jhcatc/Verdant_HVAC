import uuid
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    Date,
    DateTime,
    Text,
    Numeric
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from datetime import datetime

class Equipment(Base):

    __tablename__ = "equipment"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    company_id = Column(
        UUID(as_uuid=True),
        nullable=True
    )

    customer_id = Column(
        UUID(as_uuid=True),
        ForeignKey("customers.id"),
        nullable=True
    )

    equipment_category_id = Column(
        Integer,
        ForeignKey("equipment_categories.id"),
        nullable=False
    )

    equipment_type_id = Column(
        Integer,
        ForeignKey("equipment_types.id"),
        nullable=False
    )

    brand_id = Column(
        Integer,
        ForeignKey("equipment_brands.id"),
        nullable=False
    )

    refrigerant_type_id = Column(
        Integer,
        ForeignKey("refrigerant_types.id"),
        nullable=True
    )

    voltage_type_id = Column(
        Integer,
        ForeignKey("voltage_types.id"),
        nullable=True
    )

    power_source_id = Column(
        Integer,
        ForeignKey("power_sources.id"),
        nullable=True
    )

    installation_type_id = Column(
        Integer,
        ForeignKey("installation_types.id"),
        nullable=True
    )

    equipment_status_id = Column(
        Integer,
        ForeignKey("equipment_statuses.id"),
        nullable=False
    )

    location_id = Column(
        UUID(as_uuid=True),
        ForeignKey("customer_locations.id"),
        nullable=True
    )

    asset_tag = Column(
        String,
        unique=True,
        nullable=False
    )

    model = Column(String, nullable=True)
    serial_number = Column(String, nullable=True)

    manufacture_year = Column(
        Integer,
        nullable=True
    )

    installation_date = Column(
        Date,
        nullable=True
    )

    warranty_expiration = Column(
        Date,
        nullable=True
    )

    maintenance_interval_days = Column(
        Integer,
        nullable=True
    )

    capacity = Column(String, nullable=True)
    capacity_unit = Column(String, nullable=True)
    phase_type = Column(String, nullable=True)

    physical_location = Column(
        String,
        nullable=True
    )

    notes = Column(Text, nullable=True)

    """
    HVAC SPECIFICATIONS
    """

    seer_rating = Column(Numeric, nullable=True)
    eer_rating = Column(Numeric, nullable=True)

    last_heartbeat = Column(
        DateTime,
        nullable=True
    )

    connectivity_status = Column(
        String,
        nullable=False,
        default="offline"
    )

    cooling_capacity = Column(
        String,
        nullable=True
    )

    heating_capacity = Column(
        String,
        nullable=True
    )

    line_set_size = Column(
        String,
        nullable=True
    )

    drain_type = Column(
        String,
        nullable=True
    )

    """
    BOILER
    """

    water_capacity = Column(
        String,
        nullable=True
    )

    max_temperature = Column(
        String,
        nullable=True
    )

    working_pressure = Column(
        String,
        nullable=True
    )

    fuel_type = Column(
        String,
        nullable=True
    )

    burner_type = Column(
        String,
        nullable=True
    )

    """
    VENTILATION
    """

    airflow_cfm = Column(
        String,
        nullable=True
    )

    static_pressure = Column(
        String,
        nullable=True
    )

    duct_size = Column(
        String,
        nullable=True
    )

    fan_speed_rpm = Column(
        String,
        nullable=True
    )

    motor_hp = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    """
    RELATIONSHIPS
    """

    customer = relationship(
        "Customer",
        lazy="joined"
    )

    location = relationship(
        "CustomerLocation",
        back_populates="equipment",
        lazy="joined"
    )

    category = relationship(
        "EquipmentCategory",
        lazy="joined"
    )

    equipment_type = relationship(
        "EquipmentType",
        lazy="joined"
    )

    brand = relationship(
        "Brand",
        lazy="joined"
    )

    refrigerant = relationship(
        "RefrigerantType",
        lazy="joined"
    )

    voltage = relationship(
        "VoltageType",
        lazy="joined"
    )

    power_source = relationship(
        "PowerSource",
        lazy="joined"
    )

    installation_type = relationship(
        "InstallationType",
        lazy="joined"
    )

    equipment_status = relationship(
        "EquipmentStatus",
        lazy="joined"
    )

    photos = relationship(
        "EquipmentPhoto",
        back_populates="equipment",
        cascade="all, delete-orphan"
    )

    documents = relationship(
        "EquipmentDocument",
        back_populates="equipment",
        cascade="all, delete-orphan"
    )

    components = relationship(
        "EquipmentComponent",
        back_populates="equipment",
        cascade="all, delete-orphan"
    )

    measurements = relationship(
        "EquipmentMeasurement",
        back_populates="equipment",
        cascade="all, delete-orphan"
    )

    maintenance_logs = relationship(
        "MaintenanceLog",
        back_populates="equipment",
        cascade="all, delete-orphan"
    )

    maintenance_plans = relationship(
        "MaintenancePlanEquipment",
        back_populates="equipment",
        cascade="all, delete-orphan"
    )