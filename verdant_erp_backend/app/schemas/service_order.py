from pydantic import BaseModel, validator
from app.models.service_order import (
    ServiceOrderStatus
)


class ServiceOrderCreate(BaseModel):

    title: str
    customer_id: str
    customer_location_id: str | None = None
    equipment_id: str | None = None
    city: str | None = None
    tasks: list = []
    materials: list = []
    labor_cost: float = 0
    duration_hours: float = 1
    status: ServiceOrderStatus = "pending"
    @validator("status", pre=True)
    def normalize_status(cls, v):
        if isinstance(v, str):
            return v.lower().strip()
        return v


class ServiceOrderUpdate(BaseModel):

    status: ServiceOrderStatus | None = None