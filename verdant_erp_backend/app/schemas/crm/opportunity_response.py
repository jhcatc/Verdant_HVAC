from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OpportunityResponse(BaseModel):
    id: str
    title: str
    stage: Optional[str] = None
    estimated_value: Optional[float] = 0
    probability: Optional[int] = 0
    close_date: Optional[datetime] = None