from pydantic import BaseModel
from typing import Optional


class LeadUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    status: Optional[str] = None
    estimated_value: Optional[float] = None
    probability: Optional[int] = None
    source: Optional[str] = None
    assigned_rep: Optional[str] = None
    city: Optional[str] = None
    email: Optional[str] = None