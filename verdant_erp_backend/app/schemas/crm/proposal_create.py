from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime


class ProposalCreate(BaseModel):
    customer_id: UUID
    opportunity_id: Optional[UUID] = None
    title: str
    amount: Optional[float] = 0
    valid_until: Optional[datetime] = None