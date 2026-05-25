from pydantic import BaseModel
from typing import Optional
from datetime import date


class ContractCreate(BaseModel):
    customer_name: str
    status: Optional[str] = "ACTIVE"
    total_value: Optional[float] = 0
    sla_tier: Optional[str] = "STANDARD"
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    renewal_date: Optional[date] = None
    version: Optional[int] = 1