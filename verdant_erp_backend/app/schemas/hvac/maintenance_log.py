from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime


class EquipmentMeasurementCreate(BaseModel):
    measurement_type: str
    value: float
    unit: str


class EquipmentComponentCreate(BaseModel):
    component_name: str
    status: Optional[str] = None
    notes: Optional[str] = None


class MaintenanceLogCreate(BaseModel):
    equipment_id: UUID
    maintenance_type_id: int
    notes: Optional[str] = None
    equipment_condition: Optional[str] = None
    refrigerant_added: Optional[str] = None
    measurements: List[EquipmentMeasurementCreate] = []
    components: List[EquipmentComponentCreate] = []


class MaintenanceLogResponse(BaseModel):
    id: UUID
    equipment_id: UUID
    technician_name: str
    maintenance_type: str
    notes: Optional[str]
    equipment_condition: Optional[str]
    refrigerant_added: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True