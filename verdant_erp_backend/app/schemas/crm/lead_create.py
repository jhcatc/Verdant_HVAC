from pydantic import BaseModel
from typing import Optional


class LeadCreate(BaseModel):
    title: str
    company: str
    estimated_value: Optional[float] = 0
    probability: Optional[int] = 0
    source: Optional[str] = None
    assigned_rep: Optional[str] = None
    city: Optional[str] = None
    email: Optional[str] = None