from datetime import date
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class ComponentRegistryItemDTO(BaseModel):

    id: UUID
    equipment_id: UUID
    component_type: str
    component_name: str
    manufacturer: str | None = None
    model_number: str | None = None
    serial_number: str | None = None
    status: str
    installation_date: date | None = None
    replacement_date: date | None = None
    warranty_expiration: date | None = None
    useful_life_months: str | None = None
    failure_reason: str | None = None
    replacement_reason: str | None = None
    notes: str | None = None
    is_critical: bool
    maintenance_log_id: UUID | None = None
    created_at: datetime
    equipment_asset_tag: str | None = None
    equipment_model: str | None = None
    health_score: int
    warranty_status: str
    mtbf_days: int | None = None
    failure_events: int


class ComponentRegistrySnapshotDTO(BaseModel):

    total_components: int
    critical_components: int
    failed_components: int
    warranty_expiring: int
    average_health_score: int
    items: list[ComponentRegistryItemDTO]