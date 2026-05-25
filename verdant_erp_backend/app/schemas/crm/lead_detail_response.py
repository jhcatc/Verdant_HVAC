from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class LeadDetailResponse(BaseModel):
    id: UUID
    title: str
    company: str
    status: Optional[str] = None
    estimated_value: Optional[float] = 0
    probability: Optional[int] = 0
    source: Optional[str] = None
    assigned_rep: Optional[str] = None
    city: Optional[str] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True