from datetime import date

from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class EquipmentCreate(BaseModel):

    customer_id: Optional[UUID] = None
    location_id: Optional[UUID] = None
    equipment_category_id: int
    equipment_type_id: int
    brand_id: int
    refrigerant_type_id: Optional[int] = None
    voltage_type_id: Optional[int] = None
    power_source_id: Optional[int] = None
    installation_type_id: Optional[int] = None
    equipment_status_id: int
    asset_tag: str
    model: Optional[str] = None
    serial_number: Optional[str] = None
    manufacture_year: Optional[int] = None
    installation_date: Optional[date] = None
    warranty_expiration: Optional[date] = None
    maintenance_interval_days: Optional[int] = None
    capacity: Optional[str] = None
    capacity_unit: Optional[str] = None
    phase_type: Optional[str] = None
    equipment_location: Optional[str] = None
    notes: Optional[str] = None
    """
    HVAC
    """
    seer_rating: Optional[float] = None
    eer_rating: Optional[float] = None
    cooling_capacity: Optional[str] = None
    heating_capacity: Optional[str] = None
    line_set_size: Optional[str] = None
    drain_type: Optional[str] = None
    """
    BOILER
    """
    water_capacity: Optional[str] = None
    max_temperature: Optional[str] = None
    working_pressure: Optional[str] = None
    fuel_type: Optional[str] = None
    burner_type: Optional[str] = None
    """
    VENTILATION
    """
    airflow_cfm: Optional[str] = None
    static_pressure: Optional[str] = None
    duct_size: Optional[str] = None
    fan_speed_rpm: Optional[str] = None
    motor_hp: Optional[str] = None