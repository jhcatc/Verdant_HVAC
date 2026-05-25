from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ContractResponse(BaseModel):
    id: str
    status: Optional[str] = None
    sla_tier: Optional[str] = None
    total_value: Optional[float] = 0
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    renewal_date: Optional[datetime] = None