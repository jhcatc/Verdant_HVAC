from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class CustomerLocationCreate(BaseModel):

    customer_id: UUID
    name: str
    code: Optional[str] = None
    location_type: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    sla_tier: Optional[str] = "STANDARD"
    access_notes: Optional[str] = None
    refrigerant_notes: Optional[str] = None
    technician_notes: Optional[str] = None
    notes: Optional[str] = None


class CustomerLocationResponse(BaseModel):
    id: UUID

    customer_id: UUID
    name: str
    code: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    country: str | None = None
    contact_name: str | None = None
    contact_phone: str | None = None
    notes: str | None = None

    class Config:
        from_attributes = True