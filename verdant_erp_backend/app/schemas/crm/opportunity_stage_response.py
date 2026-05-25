from pydantic import BaseModel
from typing import Optional


class OpportunityStageResponse(BaseModel):
    id: str
    stage: str
    contract_created: bool
    contract_id: Optional[str] = None