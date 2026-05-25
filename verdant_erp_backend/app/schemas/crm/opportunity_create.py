from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OpportunityCreate(BaseModel):

    customer_id: str
    title: str
    stage: Optional[str] = "LEAD"
    probability: Optional[int] = 0
    estimated_value: Optional[float] = 0
    close_date: Optional[datetime] = None