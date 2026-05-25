from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class ProposalResponse(BaseModel):
    id: UUID
    proposal_number: str
    customer_id: UUID
    opportunity_id: Optional[UUID] = None
    source_type: str
    title: str
    status: str
    amount: float
    valid_until: Optional[datetime] = None
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True