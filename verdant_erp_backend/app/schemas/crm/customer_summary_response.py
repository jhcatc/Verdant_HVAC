from pydantic import BaseModel
from typing import Optional


class CustomerSummaryResponse(BaseModel):
    id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    annual_revenue: float
    active_contracts: int
    open_opportunities: int